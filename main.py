import os
import shutil
import re
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException, Header
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

try:
    from projects.dijital_ustabasi.cloud_storage import CloudStorage, normalize_phone
    from projects.dijital_ustabasi.parser import transcribe_audio, parse_repair_text, get_gemini_api_key
    from projects.dijital_ustabasi.pdf_generator import generate_quote_pdf
except ModuleNotFoundError:
    from cloud_storage import CloudStorage, normalize_phone
    from parser import transcribe_audio, parse_repair_text, get_gemini_api_key
    from pdf_generator import generate_quote_pdf

# Preserve Railway dynamic PORT before loading local .env file
RAILWAY_DYNAMIC_PORT = os.environ.get("PORT")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(BASE_DIR, ".env"), override=False)

PORT = int(RAILWAY_DYNAMIC_PORT or os.environ.get("PORT") or 8080)

def check_shop_access(shop: dict):
    if not shop.get("is_active", True):
        raise HTTPException(
            status_code=403,
            detail="Hesabınız askıya alınmıştır, lütfen yönetici ile iletişime geçin."
        )

    expires_at_str = shop.get("expires_at")
    if expires_at_str:
        try:
            expires_at = datetime.fromisoformat(expires_at_str)
            if datetime.now() > expires_at:
                phone = shop.get("phone_number")
                if phone:
                    storage.update_shop_active_status(phone, False)
                raise HTTPException(
                    status_code=403,
                    detail="Paket / deneme süreniz sona ermiştir. Kullanmaya devam etmek için lütfen paket talep edin."
                )
        except HTTPException as he:
            raise he
        except Exception:
            pass
    else:
        created_at_str = shop.get("created_at")
        if created_at_str:
            try:
                created_at = datetime.fromisoformat(created_at_str)
                if datetime.now() > created_at + timedelta(days=7):
                    phone = shop.get("phone_number")
                    if phone:
                        storage.update_shop_active_status(phone, False)
                    raise HTTPException(
                        status_code=403,
                        detail="7 günlük ücretsiz deneme süreniz sona ermiştir. Kullanmaya devam etmek için lütfen paket talep edin."
                    )
            except HTTPException as he:
                raise he
            except Exception:
                pass

app = FastAPI(title="Dijital Ustabaşı v1.0.0 Web Platform")

@app.middleware("http")
async def add_no_cache_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

STATIC_DIR = os.path.normpath(os.path.join(BASE_DIR, "static"))
TEMPLATES_DIR = os.path.normpath(os.path.join(BASE_DIR, "templates"))

env_storage = os.getenv("STORAGE_DIR")
if env_storage:
    if not os.path.isabs(env_storage):
        clean_storage = env_storage.replace("\\", "/").replace("projects/dijital_ustabasi/", "")
        STORAGE_DIR = os.path.abspath(os.path.join(BASE_DIR, clean_storage))
    else:
        STORAGE_DIR = os.path.normpath(env_storage)
else:
    STORAGE_DIR = os.path.normpath(os.path.join(BASE_DIR, "storage"))

try:
    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    os.makedirs(STORAGE_DIR, exist_ok=True)
except Exception:
    STORAGE_DIR = "/tmp/storage"
    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    os.makedirs(STORAGE_DIR, exist_ok=True)

if not os.path.exists(STORAGE_DIR):
    STORAGE_DIR = "/tmp/storage"
    os.makedirs(STORAGE_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/data", StaticFiles(directory=STORAGE_DIR), name="data")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

storage = CloudStorage(storage_dir=STORAGE_DIR)

class SimulateTextRequest(BaseModel):
    phone_number: str
    text: str

@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
async def get_index(request: Request):
    """
    Renders index.html (The Unified v1.0.0 Single Page App).
    """
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/admin", response_class=HTMLResponse)
async def get_admin(request: Request):
    return templates.TemplateResponse(request=request, name="admin.html")

@app.post("/api/simulate/text")
async def simulate_text(req: SimulateTextRequest):
    phone_number = normalize_phone(req.phone_number.strip())
    if not phone_number:
        phone_number = "5321234567"
        
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Mesaj metni gereklidir.")

    shop = storage.get_or_create_shop(phone_number)
    check_shop_access(shop)
    
    parsed_data = parse_repair_text(text)
    
    plaka = parsed_data.get("plaka", "PLAKASIZ")
    vehicle = parsed_data.get("vehicle", "Bilinmeyen Araç")
    items = parsed_data.get("items", [])
    usta_note = parsed_data.get("usta_note", "")

    if not items:
        return {
            "success": False,
            "message": "Metinden herhangi bir tamir işlemi veya fiyat bilgisi ayıklanamadı. Lütfen örneklere uygun yazın.",
            "parsed": parsed_data
        }

    clean_plaka = re.sub(r"[^a-zA-Z0-9]", "", plaka)
    clean_phone = re.sub(r"[^0-9]", "", phone_number)
    timestamp = f"{clean_plaka}_{clean_phone}_{os.urandom(4).hex()}"
    pdf_filename = f"teklif_{timestamp}.pdf"
    pdf_path = storage.get_pdf_path(pdf_filename)

    subtotal, vat, total, cash_total = generate_quote_pdf(
        shop_name=shop["name"],
        phone_number=shop["phone_number"],
        plaka=plaka,
        vehicle=vehicle,
        items=items,
        output_path=pdf_path,
        validity_days=7,
        custom_note=usta_note if usta_note else None
    )

    quote = storage.save_quote(
        phone_number=phone_number,
        plaka=plaka,
        vehicle=vehicle,
        items=items,
        subtotal=subtotal,
        vat=vat,
        total_price=total,
        discount_price=cash_total,
        pdf_filename=pdf_filename,
        validity_days=7,
        usta_note=usta_note
    )

    return {
        "success": True,
        "message": "Teklif başarıyla oluşturuldu.",
        "parsed": parsed_data,
        "totals": {
            "subtotal": subtotal,
            "vat": vat,
            "total": total,
            "cash_total": cash_total
        },
        "quote": quote,
        "download_url": f"/api/download/{pdf_filename}"
    }

@app.post("/api/voice/transcribe")
async def voice_transcribe(phone_number: str = Form(...), file: UploadFile = File(...)):
    phone_number = normalize_phone(phone_number.strip())
    shop = storage.get_or_create_shop(phone_number)
    check_shop_access(shop)
    
    temp_dir = os.path.join(BASE_DIR, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        transcription_text = transcribe_audio(temp_file_path)
        return {"success": True, "transcription": transcription_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ses deşifre edilemedi: {str(e)}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/api/simulate/voice")
async def simulate_voice(phone_number: str = Form(...), file: UploadFile = File(...)):
    phone_number = normalize_phone(phone_number.strip())
    if not phone_number:
        phone_number = "5321234567"

    temp_dir = os.path.join(BASE_DIR, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        transcription_text = transcribe_audio(temp_file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ses deşifre edilemedi: {str(e)}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    return {"success": True, "transcription": transcription_text}

class UpdatePackageRequest(BaseModel):
    phone_number: str
    package: str = "kalfa"

@app.post("/api/shop/package")
async def update_package(req: UpdatePackageRequest):
    phone_number = req.phone_number.strip()
    package = req.package.strip()
    shop = storage.get_shop(phone_number)
    if not shop:
        raise HTTPException(status_code=404, detail="Dükkan bulunamadı.")
    updated_shop = storage.update_shop_package(phone_number, package)
    return {"success": True, "shop": updated_shop}

class UpdateShopIdentityRequest(BaseModel):
    phone_number: str
    name: str
    logo_url: str

@app.post("/api/shop/identity")
async def update_shop_identity(req: UpdateShopIdentityRequest):
    phone_number = req.phone_number.strip()
    name = req.name.strip()
    logo_url = req.logo_url.strip()
    
    if not name:
        raise HTTPException(status_code=400, detail="Dükkan adı boş olamaz.")
        
    updated_shop = storage.update_shop_identity(phone_number, name, logo_url)
    if not updated_shop:
        raise HTTPException(status_code=404, detail="Dükkan bulunamadı.")
        
    return {"success": True, "message": "Dükkan bilgileri başarıyla güncellendi.", "shop": updated_shop}

@app.post("/api/shop/request_upgrade")
async def save_upgrade_request(req: UpdatePackageRequest):
    phone_number = req.phone_number.strip()
    package = req.package.strip()
    shop = storage.get_or_create_shop(phone_number)
    updated_shop = storage.save_shop_upgrade_request(phone_number, package)
    return {"success": True, "message": "Paket talebiniz yönetici onayına iletildi.", "shop": updated_shop}

class UpdateQuoteStatusRequest(BaseModel):
    quote_id: str
    status: str

class AssignQuotePhoneRequest(BaseModel):
    quote_id: str
    phone_number: str

@app.post("/api/quote/assign_phone")
async def assign_quote_phone(req: AssignQuotePhoneRequest):
    quote_id = req.quote_id.strip()
    phone = req.phone_number.strip()
    shop = storage.get_or_create_shop(phone)
    updated_quote = storage.assign_quote_to_shop(quote_id, phone)
    if not updated_quote:
        raise HTTPException(status_code=404, detail="Teklif bulunamadı.")
    return {"success": True, "message": "Teklif dükkanınıza bağlandı.", "quote": updated_quote, "shop": shop}

@app.post("/api/quote/status")
async def update_quote_status(req: UpdateQuoteStatusRequest):
    quote_id = req.quote_id.strip()
    status = req.status.strip()
    if status not in ["beklemede", "onaylandi", "ret"]:
        raise HTTPException(status_code=400, detail="Geçersiz durum değeri.")
    updated_quote = storage.update_quote_status(quote_id, status)
    if not updated_quote:
        raise HTTPException(status_code=404, detail="Teklif bulunamadı.")
    return {"success": True, "message": f"Teklif durumu '{status}' olarak güncellendi.", "quote": updated_quote}

class RegisterShopRequest(BaseModel):
    phone_number: str
    shop_name: str = "Oto Servis"

@app.post("/api/shop/register")
async def register_shop(req: RegisterShopRequest):
    phone = req.phone_number.strip()
    if not phone:
        raise HTTPException(status_code=400, detail="Telefon numarası zorunludur.")
    shop = storage.get_shop(phone)
    if not shop:
        shop = storage.create_shop(phone_number=phone, name=req.shop_name.strip() or "Oto Servis")
        return {"success": True, "message": "7 Günlük Ücretsiz Deneme kaydınız oluşturuldu.", "shop": shop}
    else:
        return {"success": True, "message": "Dükkan kaydınız mevcuttur.", "shop": shop}

@app.get("/api/shop")
async def get_shop_info(phone_number: str):
    shop = storage.get_shop(phone_number)
    if not shop:
        raise HTTPException(status_code=404, detail="Dükkan kaydı bulunamadı.")
    return shop

@app.get("/api/quotes")
async def get_quotes(phone_number: str = None):
    if phone_number:
        shop = storage.get_or_create_shop(phone_number)
        check_shop_access(shop)
        pkg = shop.get("package", "cirak")
        
        created_at_str = shop.get("created_at")
        is_in_trial = False
        if created_at_str:
            try:
                created_at = datetime.fromisoformat(created_at_str)
                if datetime.now() <= created_at + timedelta(days=7):
                    is_in_trial = True
            except Exception:
                pass

        all_quotes = storage.get_quotes(phone_number)
        all_quotes.sort(key=lambda q: q.get("created_at", ""), reverse=True)
        
        total_count = len(all_quotes)
        active_plates_count = len(set(q.get("plaka", "") for q in all_quotes if q.get("plaka")))
        
        # Enforce exact business logic rules:
        # Trial (7 days) or Usta package: Unlimited archive access & full analytics
        # Kalfa package: Max 15 quotes archive
        # Çırak package: Archive locked after trial (visible_quotes = [])
        if is_in_trial or pkg == "usta":
            visible_quotes = all_quotes
        elif pkg == "kalfa":
            visible_quotes = all_quotes[:15]
        else: # cirak
            visible_quotes = []
            
        return {
            "success": True,
            "total_quotes": total_count,
            "active_plates": active_plates_count,
            "quotes": visible_quotes,
            "package": pkg,
            "is_in_trial": is_in_trial
        }
    return storage.get_quotes(phone_number)

@app.get("/api/download/{filename}")
async def download_pdf(filename: str, inline: bool = False):
    pdf_path = storage.get_pdf_path(filename)
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Teklif PDF dosyası bulunamadı.")
    
    safe_filename = filename if filename.lower().endswith(".pdf") else f"{filename}.pdf"
    disposition = f'{"inline" if inline else "attachment"}; filename="{safe_filename}"'
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        headers={
            "Content-Type": "application/pdf",
            "Content-Disposition": disposition,
            "Content-Transfer-Encoding": "binary"
        }
    )

# Admin Desk Endpoints
def verify_admin_key(x_admin_key: str = Header(None, alias="X-Admin-Key")):
    expected_key = os.getenv("ADMIN_KEY", "ustabasi2026")
    if not x_admin_key or x_admin_key != expected_key:
        raise HTTPException(status_code=401, detail="Yetkisiz erişim.")

@app.get("/api/admin/shops")
async def admin_get_shops(x_admin_key: str = Header(None, alias="X-Admin-Key")):
    verify_admin_key(x_admin_key)
    return storage.get_all_shops()

@app.post("/api/admin/approve_upgrade")
async def admin_approve_upgrade(req: UpdatePackageRequest, x_admin_key: str = Header(None, alias="X-Admin-Key")):
    verify_admin_key(x_admin_key)
    phone_number = normalize_phone(req.phone_number.strip())
    shop = storage.get_shop(phone_number)
    if not shop:
        raise HTTPException(status_code=404, detail="Dükkan bulunamadı.")
    requested_pkg = shop.get("upgrade_request") or req.package or "kalfa"
    updated = storage.update_shop_package(phone_number, requested_pkg)
    storage.save_shop_upgrade_request(phone_number, None)
    return {"success": True, "shop": updated}

class ToggleActiveRequest(BaseModel):
    phone_number: str
    is_active: bool

@app.post("/api/admin/toggle_active")
async def admin_toggle_active(req: ToggleActiveRequest, x_admin_key: str = Header(None, alias="X-Admin-Key")):
    verify_admin_key(x_admin_key)
    phone_number = normalize_phone(req.phone_number.strip())
    updated = storage.update_shop_active_status(phone_number, req.is_active)
    if not updated:
        raise HTTPException(status_code=404, detail="Dükkan bulunamadı.")
    return {"success": True, "shop": updated}

class DeleteShopRequest(BaseModel):
    phone_number: str

@app.post("/api/admin/delete_shop")
async def admin_delete_shop(req: DeleteShopRequest, x_admin_key: str = Header(None, alias="X-Admin-Key")):
    verify_admin_key(x_admin_key)
    phone_number = normalize_phone(req.phone_number.strip())
    deleted = storage.delete_shop(phone_number)
    if not deleted:
        raise HTTPException(status_code=404, detail="Dükkan bulunamadı.")
    return {"success": True, "message": "Dükkan ve tüm teklifleri kalıcı olarak silindi."}

class SetExpirationRequest(BaseModel):
    phone_number: str
    expires_at: str

@app.post("/api/admin/set_expiration")
async def admin_set_expiration(req: SetExpirationRequest, x_admin_key: str = Header(None, alias="X-Admin-Key")):
    verify_admin_key(x_admin_key)
    phone_number = normalize_phone(req.phone_number.strip())
    try:
        dt = datetime.strptime(req.expires_at.strip(), "%Y-%m-%d")
        dt_end = datetime(dt.year, dt.month, dt.day, 23, 59, 59)
        updated = storage.update_shop_expiration(phone_number, dt_end.isoformat())
        if not updated:
            raise HTTPException(status_code=404, detail="Dükkan bulunamadı.")
        return {"success": True, "shop": updated}
    except ValueError:
        raise HTTPException(status_code=400, detail="Geçersiz tarih formatı. YYYY-MM-DD kullanılmalı.")

class ExtendTrialRequest(BaseModel):
    phone_number: str
    days: int

@app.post("/api/admin/extend_trial")
async def admin_extend_trial(req: ExtendTrialRequest, x_admin_key: str = Header(None, alias="X-Admin-Key")):
    verify_admin_key(x_admin_key)
    phone_number = normalize_phone(req.phone_number.strip())
    updated = storage.extend_shop_expiration(phone_number, req.days)
    if not updated:
        raise HTTPException(status_code=404, detail="Dükkan bulunamadı.")
    return {"success": True, "shop": updated}

@app.post("/api/admin/reset_database")
async def admin_reset_database(x_admin_key: str = Header(None, alias="X-Admin-Key")):
    verify_admin_key(x_admin_key)
    storage._save_db({"shops": {}, "quotes": []})
    return {"success": True, "message": "Veritabanı ve tüm kayıtlar sıfırlandı."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
