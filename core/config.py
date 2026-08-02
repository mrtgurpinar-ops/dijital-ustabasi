import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_app_version() -> str:
    """
    Dynamically resolves application version from version.txt or CHANGELOG.md.
    """
    version_file = os.path.join(BASE_DIR, "version.txt")
    if os.path.exists(version_file):
        try:
            with open(version_file, "r", encoding="utf-8") as f:
                v = f.read().strip()
                if v:
                    return v
        except Exception:
            pass

    changelog_file = os.path.join(BASE_DIR, "CHANGELOG.md")
    if os.path.exists(changelog_file):
        try:
            with open(changelog_file, "r", encoding="utf-8") as f:
                content = f.read()
                match = re.search(r"##\s*\[v?(\d+\.\d+\.\d+)\]", content)
                if match:
                    return match.group(1)
        except Exception:
            pass

    return "1.15.0"

APP_NAME = "Dijital Ustabaşı"
DEFAULT_ADMIN_PHONE = "5555105635"
