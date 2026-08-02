import os
import sys
import json
import urllib.request

RAILWAY_GRAPHQL_URL = "https://backboard.railway.com/graphql/v2"

class RailwayAPI:
    def __init__(self, token=None):
        self.token = token or os.environ.get("RAILWAY_TOKEN")
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "DijitalUstabasi-RailwayCLI/1.0"
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def _query(self, query_str, variables=None):
        payload = json.dumps({"query": query_str, "variables": variables or {}}).encode("utf-8")
        req = urllib.request.Request(RAILWAY_GRAPHQL_URL, data=payload, headers=self.headers)
        try:
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result
        except Exception as e:
            return {"error": str(e)}

    def get_me(self):
        query = """
        query me {
            me {
                id
                name
                email
            }
        }
        """
        return self._query(query)

    def get_project(self, project_id):
        query = """
        query project($id: String!) {
            project(id: $id) {
                id
                name
                services {
                    edges {
                        node {
                            id
                            name
                        }
                    }
                }
            }
        }
        """
        return self._query(query, {"id": project_id})

    def check_health(self, target_url="https://dijital-ustabasi-production.up.railway.app/"):
        req = urllib.request.Request(target_url, headers={"User-Agent": "HealthCheck/1.0"})
        try:
            with urllib.request.urlopen(req) as resp:
                return {
                    "status_code": resp.getcode(),
                    "healthy": resp.getcode() == 200,
                    "url": target_url
                }
        except Exception as e:
            return {"status_code": 500, "healthy": False, "error": str(e), "url": target_url}

if __name__ == "__main__":
    api = RailwayAPI()
    print("--- Railway Health Check ---")
    health = api.check_health()
    print(json.dumps(health, indent=2, ensure_ascii=False))

    if api.token:
        print("\n--- Railway Profile Info ---")
        print(json.dumps(api.get_me(), indent=2, ensure_ascii=False))
    else:
        print("\n[Info] RAILWAY_TOKEN henüz tanımlanmadı. API çağrıları için token eklendiğinde tam yönetim aktifleşecektir.")
