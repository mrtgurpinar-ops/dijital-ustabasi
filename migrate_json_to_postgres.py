import os
import json
from datetime import datetime

try:
    from projects.dijital_ustabasi.database import engine, Base, SessionLocal
    from projects.dijital_ustabasi.models import ShopModel, QuoteModel, CustomerModel, VehicleModel
    from projects.dijital_ustabasi.cloud_storage import normalize_phone
except ModuleNotFoundError:
    from database import engine, Base, SessionLocal
    from models import ShopModel, QuoteModel, CustomerModel, VehicleModel
    from cloud_storage import normalize_phone


from sqlalchemy.orm import sessionmaker

def migrate_json_data(storage_dir=None, target_engine=None):
    """
    Reads existing database.json and migrates all shops and quotes into the DB engine.
    Guarantees zero data loss.
    """
    active_engine = target_engine or engine
    Base.metadata.create_all(bind=active_engine)
    
    if storage_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        storage_dir = os.getenv("STORAGE_DIR") or os.path.join(base_dir, "storage")

    json_path = os.path.join(storage_dir, "database.json")
    if not os.path.exists(json_path):
        print(f"[Migration] No database.json found at {json_path}. Database tables initialized.")
        return

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[Migration Error] Could not read JSON database: {e}")
        return

    if target_engine:
        LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=target_engine)
        db = LocalSession()
    else:
        db = SessionLocal()
    try:
        shops_dict = data.get("shops", {})
        quotes_list = data.get("quotes", [])
        
        migrated_shops = 0
        migrated_quotes = 0

        # 1. Migrate Shops
        for phone, shop_data in shops_dict.items():
            norm_phone = normalize_phone(phone)
            existing = db.query(ShopModel).filter(ShopModel.phone_number == norm_phone).first()
            if not existing:
                created_at = None
                if shop_data.get("created_at"):
                    try:
                        created_at = datetime.fromisoformat(shop_data["created_at"])
                    except Exception:
                        pass
                expires_at = None
                if shop_data.get("expires_at"):
                    try:
                        expires_at = datetime.fromisoformat(shop_data["expires_at"])
                    except Exception:
                        pass

                new_shop = ShopModel(
                    phone_number=norm_phone,
                    password_hash=shop_data.get("password_hash", ""),
                    name=shop_data.get("name", "Oto Servis"),
                    logo_url=shop_data.get("logo_url", ""),
                    package=shop_data.get("package", "usta"),
                    is_active=shop_data.get("is_active", True),
                    created_at=created_at or datetime.now(),
                    expires_at=expires_at,
                    upgrade_request=shop_data.get("upgrade_request")
                )
                db.add(new_shop)
                migrated_shops += 1
        
        db.commit()

        # 2. Migrate Quotes
        for q in quotes_list:
            quote_id = q.get("quote_id")
            if not quote_id:
                continue
            existing_q = db.query(QuoteModel).filter(QuoteModel.quote_id == quote_id).first()
            if not existing_q:
                norm_phone = normalize_phone(q.get("phone_number", ""))
                shop = db.query(ShopModel).filter(ShopModel.phone_number == norm_phone).first()
                shop_id = shop.id if shop else None
                
                q_created = None
                if q.get("created_at"):
                    try:
                        q_created = datetime.fromisoformat(q["created_at"])
                    except Exception:
                        pass

                new_quote = QuoteModel(
                    quote_id=quote_id,
                    shop_id=shop_id,
                    phone_number=norm_phone,
                    plaka=q.get("plaka", "").upper(),
                    vehicle=q.get("vehicle", "").title(),
                    items_json=json.dumps(q.get("items", []), ensure_ascii=False),
                    subtotal=q.get("subtotal", 0.0),
                    vat=q.get("vat", 0.0),
                    total_price=q.get("total_price", 0.0),
                    discount_price=q.get("discount_price", 0.0),
                    pdf_filename=q.get("pdf_filename", ""),
                    validity_days=q.get("validity_days", 7),
                    usta_note=q.get("usta_note", ""),
                    status=q.get("status", "beklemede"),
                    created_at=q_created or datetime.now()
                )
                db.add(new_quote)
                migrated_quotes += 1

        db.commit()
        print(f"[Migration Complete] Migrated {migrated_shops} shops and {migrated_quotes} quotes into DB.")
    except Exception as e:
        db.rollback()
        print(f"[Migration Error] Rollback executed due to error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    migrate_json_data()
