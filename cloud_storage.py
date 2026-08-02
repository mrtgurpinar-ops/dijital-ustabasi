import os
import json
import re
import threading
from datetime import datetime, timedelta

def normalize_phone(phone: str) -> str:
    """
    Normalizes Turkish phone numbers to a standard 10-digit format (e.g. 5321234567).
    """
    if not phone:
        return ""
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 12 and digits.startswith("90"):
        return digits[2:]
    if len(digits) == 11 and digits.startswith("0"):
        return digits[1:]
    if len(digits) >= 10:
        return digits[-10:]
    return digits

class CloudStorage:
    def __init__(self, storage_dir=None):
        self._lock = threading.Lock()
        if storage_dir is None:
            env_dir = os.environ.get("STORAGE_DIR")
            if env_dir:
                self.storage_dir = env_dir
            else:
                self.storage_dir = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "storage"
                )
        else:
            self.storage_dir = storage_dir

        self.pdf_dir = os.path.join(self.storage_dir, "pdfs")
        self.db_path = os.path.join(self.storage_dir, "database.json")
        
        os.makedirs(self.storage_dir, exist_ok=True)
        os.makedirs(self.pdf_dir, exist_ok=True)
        
        if not os.path.exists(self.db_path):
            self._save_db({"shops": {}, "quotes": []})

    def _read_db(self):
        with self._lock:
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._cached_db = data
                    return data
            except Exception:
                if hasattr(self, "_cached_db") and self._cached_db:
                    return self._cached_db
                return {"shops": {}, "quotes": []}

    def _save_db(self, data):
        with self._lock:
            self._cached_db = data
            try:
                with open(self.db_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print("DB save error:", e)

    def get_shop(self, phone_number):
        phone_number = normalize_phone(phone_number)
        db = self._read_db()
        return db["shops"].get(phone_number)

    def create_shop(self, phone_number, name="Oto Servis", logo_url=""):
        phone_number = normalize_phone(phone_number)
        db = self._read_db()
        now = datetime.now()
        expires = now + timedelta(days=7)
        shop = {
            "phone_number": phone_number,
            "name": name,
            "logo_url": logo_url,
            "package": "usta",  # Deneme süresi usta olarak başlar
            "is_active": True,
            "created_at": now.isoformat(),
            "expires_at": expires.isoformat(),
            "upgrade_request": None
        }
        db["shops"][phone_number] = shop
        self._save_db(db)
        return shop

    def get_or_create_shop(self, phone_number):
        phone_number = normalize_phone(phone_number)
        if not phone_number:
            phone_number = "5321234567"
        shop = self.get_shop(phone_number)
        if not shop:
            shop = self.create_shop(phone_number)
        return shop

    def update_shop_package(self, phone_number, package):
        phone_number = normalize_phone(phone_number)
        if package not in ["cirak", "kalfa", "usta"]:
            package = "cirak"
        db = self._read_db()
        if phone_number in db["shops"]:
            db["shops"][phone_number]["package"] = package
            self._save_db(db)
            return db["shops"][phone_number]
        return None

    def update_shop_expiration(self, phone_number, expires_at_iso: str):
        phone_number = normalize_phone(phone_number)
        db = self._read_db()
        if phone_number in db["shops"]:
            db["shops"][phone_number]["expires_at"] = expires_at_iso
            db["shops"][phone_number]["is_active"] = True
            self._save_db(db)
            return db["shops"][phone_number]
        return None

    def extend_shop_expiration(self, phone_number, days: int):
        phone_number = normalize_phone(phone_number)
        db = self._read_db()
        if phone_number in db["shops"]:
            shop = db["shops"][phone_number]
            current_exp = shop.get("expires_at")
            base_dt = datetime.now()
            if current_exp:
                try:
                    exp_dt = datetime.fromisoformat(current_exp)
                    if exp_dt > base_dt:
                        base_dt = exp_dt
                except Exception:
                    pass
            new_exp = base_dt + timedelta(days=days)
            shop["expires_at"] = new_exp.isoformat()
            shop["is_active"] = True
            self._save_db(db)
            return shop
        return None

    def update_shop_active_status(self, phone_number, is_active: bool):
        phone_number = normalize_phone(phone_number)
        db = self._read_db()
        if phone_number in db["shops"]:
            db["shops"][phone_number]["is_active"] = is_active
            self._save_db(db)
            return db["shops"][phone_number]
        return None

    def delete_shop(self, phone_number):
        phone_number = normalize_phone(phone_number)
        db = self._read_db()
        deleted = False
        if phone_number in db["shops"]:
            del db["shops"][phone_number]
            deleted = True
        
        # Also remove quotes belonging to this phone number
        db["quotes"] = [q for q in db.get("quotes", []) if q.get("phone_number") != phone_number]
        if deleted:
            self._save_db(db)
            return True
        return False

    def update_shop_identity(self, phone_number, name, logo_url, created_at=None):
        phone_number = normalize_phone(phone_number)
        db = self._read_db()
        if phone_number in db["shops"]:
            db["shops"][phone_number]["name"] = name
            db["shops"][phone_number]["logo_url"] = logo_url
            if created_at:
                db["shops"][phone_number]["created_at"] = created_at
            self._save_db(db)
            return db["shops"][phone_number]
        return None

    def save_shop_upgrade_request(self, phone_number, requested_package):
        phone_number = normalize_phone(phone_number)
        db = self._read_db()
        if phone_number in db["shops"]:
            db["shops"][phone_number]["upgrade_request"] = requested_package
            self._save_db(db)
            return db["shops"][phone_number]
        return None

    def save_quote(self, phone_number, plaka, vehicle, items, subtotal, vat, total_price, discount_price, pdf_filename, validity_days=7, usta_note=""):
        phone_number = normalize_phone(phone_number)
        db = self._read_db()
        created_at = datetime.now().isoformat()
        
        quote = {
            "quote_id": f"Q-{datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]}",
            "phone_number": phone_number,
            "plaka": plaka.upper(),
            "vehicle": vehicle.strip().title(),
            "items": items,
            "subtotal": subtotal,
            "vat": vat,
            "total_price": total_price,
            "discount_price": discount_price,
            "pdf_filename": pdf_filename,
            "created_at": created_at,
            "validity_days": validity_days,
            "usta_note": usta_note,
            "status": "beklemede"
        }
        
        db["quotes"].append(quote)
        self._save_db(db)
        return quote

    def assign_quote_to_shop(self, quote_id, phone_number):
        phone_number = normalize_phone(phone_number)
        db = self._read_db()
        for q in db["quotes"]:
            if q.get("quote_id") == quote_id:
                q["phone_number"] = phone_number
                self._save_db(db)
                return q
        return None

    def update_quote_status(self, quote_id, status):
        db = self._read_db()
        for quote in db["quotes"]:
            if quote.get("quote_id") == quote_id:
                quote["status"] = status
                self._save_db(db)
                return quote
        return None

    def get_quotes(self, phone_number=None):
        db = self._read_db()
        if phone_number:
            norm_target = normalize_phone(phone_number)
            return [q for q in db["quotes"] if normalize_phone(q.get("phone_number", "")) == norm_target]
        return db["quotes"]

    def get_phone_number_by_pdf(self, pdf_filename):
        db = self._read_db()
        for q in db["quotes"]:
            if q.get("pdf_filename") == pdf_filename:
                return q.get("phone_number")
        return None

    def get_pdf_path(self, filename):
        return os.path.join(self.pdf_dir, filename)

    def get_all_shops(self):
        db = self._read_db()
        return db.get("shops", {})
