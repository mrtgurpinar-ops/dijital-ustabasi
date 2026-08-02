import os
import json
import re
import threading
import hashlib
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    from projects.dijital_ustabasi.database import Base
    from projects.dijital_ustabasi.models import ShopModel, QuoteModel, CustomerModel, VehicleModel
except ModuleNotFoundError:
    from database import Base
    from models import ShopModel, QuoteModel, CustomerModel, VehicleModel


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


def hash_password(password: str) -> str:
    if not password:
        return ""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


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

        try:
            from projects.dijital_ustabasi.database import engine, SessionLocal, Base
        except ModuleNotFoundError:
            from database import engine, SessionLocal, Base

        if storage_dir and storage_dir != os.getenv("STORAGE_DIR"):
            sqlite_file = os.path.join(self.storage_dir, "test_db.db")
            self.engine = create_engine(f"sqlite:///{sqlite_file}", connect_args={"check_same_thread": False})
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        else:
            self.engine = engine
            self.SessionLocal = SessionLocal
        
        # Initialize Database Tables
        try:
            Base.metadata.create_all(bind=self.engine)
            try:
                from projects.dijital_ustabasi.migrate_json_to_postgres import migrate_json_data
            except ModuleNotFoundError:
                from migrate_json_to_postgres import migrate_json_data
            migrate_json_data(self.storage_dir, target_engine=self.engine)
            self.init_five_tier_accounts()
        except Exception as e:
            print("[CloudStorage Engine Warning]", e)

        if not os.path.exists(self.db_path):
            self._save_db({"shops": {}, "quotes": []})

    def init_five_tier_accounts(self):
        now = datetime.now()
        default_accounts = [
            {
                "phone": "5555105635",
                "password": "DijitalAdmin2026!",
                "name": "👑 Süper Admin Servis",
                "package": "usta",
                "expires_at": None
            }
        ]

        db_session = self._get_session()
        try:
            for acc in default_accounts:
                phone = acc["phone"]
                shop = db_session.query(ShopModel).filter(ShopModel.phone_number == phone).first()
                if not shop:
                    shop = ShopModel(
                        phone_number=phone,
                        password_hash=hash_password(acc["password"]),
                        name=acc["name"],
                        logo_url="",
                        package=acc["package"],
                        is_active=True,
                        created_at=now,
                        expires_at=acc["expires_at"],
                        upgrade_request=None
                    )
                    db_session.add(shop)
                else:
                    shop.password_hash = hash_password(acc["password"])
                    shop.package = acc["package"]
                    shop.is_active = True
                    if acc["expires_at"] is not None:
                        shop.expires_at = acc["expires_at"]
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            print("[Five Tier Setup Error]", e)
        finally:
            db_session.close()

    def _get_session(self):
        return self.SessionLocal()

    def _read_db(self):
        with self._lock:
            db_session = self._get_session()
            try:
                shops_orm = db_session.query(ShopModel).all()
                quotes_orm = db_session.query(QuoteModel).all()
                
                shops_dict = {s.phone_number: s.to_dict() for s in shops_orm}
                quotes_list = [q.to_dict() for q in quotes_orm]
                return {"shops": shops_dict, "quotes": quotes_list}
            except Exception as e:
                try:
                    with open(self.db_path, "r", encoding="utf-8") as f:
                        return json.load(f)
                except Exception:
                    return {"shops": {}, "quotes": []}
            finally:
                db_session.close()

    def _save_db(self, data):
        with self._lock:
            try:
                with open(self.db_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print("JSON file backup write error:", e)

    def get_shop(self, phone_number):
        phone_number = normalize_phone(phone_number)
        db_session = self._get_session()
        try:
            shop_orm = db_session.query(ShopModel).filter(ShopModel.phone_number == phone_number).first()
            return shop_orm.to_dict() if shop_orm else None
        finally:
            db_session.close()

    def create_shop(self, phone_number, password="", name="Oto Servis", logo_url=""):
        phone_number = normalize_phone(phone_number)
        now = datetime.now()
        expires = now + timedelta(days=7)

        db_session = self._get_session()
        try:
            shop_orm = db_session.query(ShopModel).filter(ShopModel.phone_number == phone_number).first()
            if not shop_orm:
                shop_orm = ShopModel(
                    phone_number=phone_number,
                    password_hash=hash_password(password),
                    name=name,
                    logo_url=logo_url,
                    package="usta",
                    is_active=True,
                    created_at=now,
                    expires_at=expires,
                    upgrade_request=None
                )
                db_session.add(shop_orm)
                db_session.commit()
                db_session.refresh(shop_orm)
            res = shop_orm.to_dict()
        finally:
            db_session.close()

        # Dual backup to JSON
        full_data = self._read_db()
        full_data["shops"][phone_number] = res
        self._save_db(full_data)
        return res

    def verify_shop_login(self, phone_number, password=""):
        phone_number = normalize_phone(phone_number)
        db_session = self._get_session()
        try:
            shop_orm = db_session.query(ShopModel).filter(ShopModel.phone_number == phone_number).first()
            if not shop_orm:
                return False, "Dükkan kaydı bulunamadı. Lütfen kayıt olun veya ücretsiz deneme başlatın.", None
            
            stored_hash = shop_orm.password_hash
            if not stored_hash:
                if password:
                    shop_orm.password_hash = hash_password(password)
                    db_session.commit()
                return True, "Giriş başarılı (İlk şifre tanımlandı).", shop_orm.to_dict()

            if stored_hash == hash_password(password):
                return True, "Giriş başarılı.", shop_orm.to_dict()
            
            return False, "Hatalı şifre! Lütfen şifrenizi kontrol ediniz.", None
        finally:
            db_session.close()

    def update_shop_password(self, phone_number, new_password):
        phone_number = normalize_phone(phone_number)
        db_session = self._get_session()
        try:
            shop_orm = db_session.query(ShopModel).filter(ShopModel.phone_number == phone_number).first()
            if shop_orm:
                shop_orm.password_hash = hash_password(new_password)
                db_session.commit()
                return shop_orm.to_dict()
            return None
        finally:
            db_session.close()

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

        db_session = self._get_session()
        try:
            shop_orm = db_session.query(ShopModel).filter(ShopModel.phone_number == phone_number).first()
            if shop_orm:
                shop_orm.package = package
                db_session.commit()
                return shop_orm.to_dict()
            return None
        finally:
            db_session.close()

    def update_shop_expiration(self, phone_number, expires_at_iso: str):
        phone_number = normalize_phone(phone_number)
        db_session = self._get_session()
        try:
            shop_orm = db_session.query(ShopModel).filter(ShopModel.phone_number == phone_number).first()
            if shop_orm:
                shop_orm.expires_at = datetime.fromisoformat(expires_at_iso)
                shop_orm.is_active = True
                db_session.commit()
                return shop_orm.to_dict()
            return None
        finally:
            db_session.close()

    def extend_shop_expiration(self, phone_number, days: int):
        phone_number = normalize_phone(phone_number)
        db_session = self._get_session()
        try:
            shop_orm = db_session.query(ShopModel).filter(ShopModel.phone_number == phone_number).first()
            if shop_orm:
                base_dt = datetime.now()
                if shop_orm.expires_at and shop_orm.expires_at > base_dt:
                    base_dt = shop_orm.expires_at
                shop_orm.expires_at = base_dt + timedelta(days=days)
                shop_orm.is_active = True
                db_session.commit()
                return shop_orm.to_dict()
            return None
        finally:
            db_session.close()

    def update_shop_active_status(self, phone_number, is_active: bool):
        phone_number = normalize_phone(phone_number)
        db_session = self._get_session()
        try:
            shop_orm = db_session.query(ShopModel).filter(ShopModel.phone_number == phone_number).first()
            if shop_orm:
                shop_orm.is_active = is_active
                db_session.commit()
                return shop_orm.to_dict()
            return None
        finally:
            db_session.close()

    def delete_shop(self, phone_number):
        phone_number = normalize_phone(phone_number)
        db_session = self._get_session()
        try:
            shop_orm = db_session.query(ShopModel).filter(ShopModel.phone_number == phone_number).first()
            if shop_orm:
                db_session.delete(shop_orm)
                db_session.commit()
                return True
            return False
        finally:
            db_session.close()

    def update_shop_identity(self, phone_number, name, logo_url, created_at=None):
        phone_number = normalize_phone(phone_number)
        db_session = self._get_session()
        try:
            shop_orm = db_session.query(ShopModel).filter(ShopModel.phone_number == phone_number).first()
            if shop_orm:
                shop_orm.name = name
                shop_orm.logo_url = logo_url
                if created_at:
                    try:
                        clean_created = created_at.replace("Z", "")
                        shop_orm.created_at = datetime.fromisoformat(clean_created)
                    except Exception:
                        pass
                db_session.commit()
                return shop_orm.to_dict()
            return None
        finally:
            db_session.close()

    def save_shop_upgrade_request(self, phone_number, requested_package):
        phone_number = normalize_phone(phone_number)
        db_session = self._get_session()
        try:
            shop_orm = db_session.query(ShopModel).filter(ShopModel.phone_number == phone_number).first()
            if shop_orm:
                shop_orm.upgrade_request = requested_package
                db_session.commit()
                return shop_orm.to_dict()
            return None
        finally:
            db_session.close()

    def save_quote(self, phone_number, plaka, vehicle, items, subtotal, vat, total_price, discount_price, pdf_filename, validity_days=7, usta_note=""):
        phone_number = normalize_phone(phone_number)
        quote_id = f"Q-{datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]}"

        db_session = self._get_session()
        try:
            shop = db_session.query(ShopModel).filter(ShopModel.phone_number == phone_number).first()
            shop_id = shop.id if shop else None

            quote_orm = QuoteModel(
                quote_id=quote_id,
                shop_id=shop_id,
                phone_number=phone_number,
                plaka=plaka.upper(),
                vehicle=vehicle.strip().title(),
                subtotal=subtotal,
                vat=vat,
                total_price=total_price,
                discount_price=discount_price,
                pdf_filename=pdf_filename,
                validity_days=validity_days,
                usta_note=usta_note,
                status="beklemede",
                created_at=datetime.now()
            )
            quote_orm.set_items(items)
            db_session.add(quote_orm)
            db_session.commit()
            db_session.refresh(quote_orm)
            res = quote_orm.to_dict()
        finally:
            db_session.close()

        # Dual backup to JSON
        full_data = self._read_db()
        full_data["quotes"].append(res)
        self._save_db(full_data)
        return res

    def assign_quote_to_shop(self, quote_id, phone_number):
        phone_number = normalize_phone(phone_number)
        db_session = self._get_session()
        try:
            quote_orm = db_session.query(QuoteModel).filter(QuoteModel.quote_id == quote_id).first()
            if quote_orm:
                quote_orm.phone_number = phone_number
                shop = db_session.query(ShopModel).filter(ShopModel.phone_number == phone_number).first()
                if shop:
                    quote_orm.shop_id = shop.id
                db_session.commit()
                return quote_orm.to_dict()
            return None
        finally:
            db_session.close()

    def update_quote_status(self, quote_id, status):
        db_session = self._get_session()
        try:
            quote_orm = db_session.query(QuoteModel).filter(QuoteModel.quote_id == quote_id).first()
            if quote_orm:
                quote_orm.status = status
                db_session.commit()
                return quote_orm.to_dict()
            return None
        finally:
            db_session.close()

    def get_quote_by_id(self, quote_id):
        db_session = self._get_session()
        try:
            quote_orm = db_session.query(QuoteModel).filter(QuoteModel.quote_id == quote_id).first()
            return quote_orm.to_dict() if quote_orm else None
        finally:
            db_session.close()

    def get_quotes(self, phone_number=None):
        db_session = self._get_session()
        try:
            if phone_number:
                norm_target = normalize_phone(phone_number)
                quotes_orm = db_session.query(QuoteModel).filter(QuoteModel.phone_number == norm_target).all()
            else:
                quotes_orm = db_session.query(QuoteModel).all()
            return [q.to_dict() for q in quotes_orm]
        finally:
            db_session.close()

    def get_phone_number_by_pdf(self, pdf_filename):
        db_session = self._get_session()
        try:
            quote_orm = db_session.query(QuoteModel).filter(QuoteModel.pdf_filename == pdf_filename).first()
            return quote_orm.phone_number if quote_orm else None
        finally:
            db_session.close()

    def get_pdf_path(self, filename):
        return os.path.join(self.pdf_dir, filename)

    def get_all_shops(self):
        db_session = self._get_session()
        try:
            shops_orm = db_session.query(ShopModel).all()
            return {s.phone_number: s.to_dict() for s in shops_orm}
        finally:
            db_session.close()
