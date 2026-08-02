import os
import json
import urllib.request
import urllib.error
from datetime import datetime

try:
    from projects.dijital_ustabasi.cloud_storage import CloudStorage, normalize_phone
    from projects.dijital_ustabasi.parser import parse_repair_text, transcribe_audio
    from projects.dijital_ustabasi.pdf_generator import generate_quote_pdf
except ModuleNotFoundError:
    from cloud_storage import CloudStorage, normalize_phone
    from parser import parse_repair_text, transcribe_audio
    from pdf_generator import generate_quote_pdf

storage = CloudStorage()

def get_whatsapp_token() -> str:
    return os.getenv("WHATSAPP_TOKEN", "")

def get_whatsapp_phone_id() -> str:
    return os.getenv("WHATSAPP_PHONE_ID", "")

def get_whatsapp_verify_token() -> str:
    return os.getenv("WHATSAPP_VERIFY_TOKEN", "ustabasi_verify_secret_2026")

def send_whatsapp_message(to_phone: str, text: str) -> dict:
    """
    Sends a text message to a WhatsApp user using Meta WhatsApp Business Cloud API.
    If credentials are missing, logs and returns a mock success payload.
    """
    token = get_whatsapp_token()
    phone_id = get_whatsapp_phone_id()
    
    clean_phone = normalize_phone(to_phone)
    if not clean_phone.startswith("90") and len(clean_phone) == 10:
        full_whatsapp_phone = f"90{clean_phone}"
    else:
        full_whatsapp_phone = clean_phone

    if not token or not phone_id:
        try:
            print(f"[WhatsApp Bot Mock Send] To: {full_whatsapp_phone} | Msg:\n{text}")
        except Exception:
            pass
        return {"success": True, "mock": True, "to": full_whatsapp_phone, "text": text}
        
    url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": full_whatsapp_phone,
        "type": "text",
        "text": {
            "preview_url": True,
            "body": text
        }
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except Exception as e:
        print(f"WhatsApp API Send Error: {str(e)}")
        return {"success": False, "error": str(e)}

def download_whatsapp_media(media_id: str) -> bytes:
    """
    Downloads media (audio/voice note) bytes from Meta WhatsApp Graph API.
    """
    token = get_whatsapp_token()
    if not token or not media_id:
        return b""
        
    try:
        url_info = f"https://graph.facebook.com/v18.0/{media_id}"
        req_info = urllib.request.Request(url_info, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req_info, timeout=10) as resp_info:
            data_info = json.loads(resp_info.read().decode("utf-8"))
            media_url = data_info.get("url")
            
        if not media_url:
            return b""
            
        req_media = urllib.request.Request(media_url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req_media, timeout=20) as resp_media:
            return resp_media.read()
    except Exception as e:
        print(f"WhatsApp Media Download Error: {str(e)}")
        return b""

def process_whatsapp_quote_request(phone_number: str, message_text: str = "", audio_bytes: bytes = None, domain_host: str = "dijital-ustabasi-production.up.railway.app") -> dict:
    """
    Core engine: processes text or voice note, generates PDF quote, stores in database,
    and returns response message dict + sends WhatsApp reply.
    """
    clean_phone = normalize_phone(phone_number)
    shop = storage.get_or_create_shop(clean_phone)
    shop_name = shop.get("name", f"Usta ({clean_phone})")
    
    parsed_data = None
    if audio_bytes and len(audio_bytes) > 0:
        temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
        os.makedirs(temp_dir, exist_ok=True)
        temp_audio_path = os.path.join(temp_dir, f"whatsapp_voice_{clean_phone}_{datetime.now().strftime('%Y%m%d%H%M%S')}.ogg")
        try:
            with open(temp_audio_path, "wb") as f:
                f.write(audio_bytes)
            transcription = transcribe_audio(temp_audio_path)
            if transcription:
                parsed_data = parse_repair_text(transcription)
        except Exception as e:
            try:
                print(f"[WhatsApp Voice Process Error] {str(e)}")
            except Exception:
                pass
        finally:
            if os.path.exists(temp_audio_path):
                try:
                    os.remove(temp_audio_path)
                except Exception:
                    pass
            
    if not parsed_data and message_text:
        parsed_data = parse_repair_text(message_text)
        
    if not parsed_data or not parsed_data.get("items"):
        error_msg = f"⚠️ *DİJİTAL USTABAŞI BOT*\n\nMerhaba *{shop_name}*,\nMesajınızdan veya ses kaydınızdan yapılan işler ve fiyatlar okunamadı.\n\n*Örnek Sesli / Yazılı Mesaj:* \n_\"34 ABC 123 Fiat Egea ön fren balatası 1500 TL yağ bakımı 2500 TL usta notu orijinal parça kullanıldı\"_\n\nLütfen tekrar deneyin!"
        send_whatsapp_message(clean_phone, error_msg)
        return {"success": False, "message": error_msg}

    plaka = parsed_data.get("plaka", "PLAKASIZ")
    vehicle = parsed_data.get("vehicle", "Bilinmeyen Araç")
    items = parsed_data.get("items", [])
    usta_note = parsed_data.get("usta_note", "")
    
    subtotal = sum(float(item.get("price", 0)) for item in items)
    vat = subtotal * 0.20
    total_price = subtotal + vat
    discount_price = total_price * 0.90 # %10 Nakit Ödeme İndirimi
    
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"teklif_{clean_phone}_{now_str}.pdf"
    pdf_path = storage.get_pdf_path(pdf_filename)
    
    quote_payload = {
        "shop_name": shop_name,
        "phone_number": clean_phone,
        "plaka": plaka,
        "vehicle": vehicle,
        "items": items,
        "subtotal": subtotal,
        "vat": vat,
        "total_price": total_price,
        "discount_price": discount_price,
        "created_at": datetime.now().isoformat(),
        "validity_days": 7,
        "usta_note": usta_note
    }
    
    logo_path = None
    if shop.get("logo_url"):
        candidate_logo = os.path.join(storage.storage_dir, "logos", os.path.basename(shop["logo_url"]))
        if os.path.exists(candidate_logo):
            logo_path = candidate_logo
            
    generate_quote_pdf(
        shop_name=shop_name,
        phone_number=clean_phone,
        plaka=plaka,
        vehicle=vehicle,
        items=items,
        output_path=pdf_path,
        validity_days=7,
        custom_note=usta_note
    )
    
    saved_quote = storage.save_quote(
        phone_number=clean_phone,
        plaka=plaka,
        vehicle=vehicle,
        items=items,
        subtotal=subtotal,
        vat=vat,
        total_price=total_price,
        discount_price=discount_price,
        pdf_filename=pdf_filename,
        validity_days=7,
        usta_note=usta_note
    )
    
    if not domain_host.startswith("http"):
        base_url = f"https://{domain_host}"
    else:
        base_url = domain_host
        
    pdf_url = f"{base_url}/api/download/{pdf_filename}"
    dashboard_url = f"{base_url}/dashboard?login_phone={clean_phone}"
    
    items_formatted = ""
    for idx, item in enumerate(items, 1):
        desc = item.get("description", "İşlem")
        p = item.get("price", 0)
        items_formatted += f"  {idx}. {desc}: *{p:,.2f} TL*\n"
        
    response_msg = f"""🛠️ *DİJİTAL USTABAŞI - TEKLİFİNİZ HAZIR!*
----------------------------------------
🚗 *Araç:* {vehicle}
🏷️ *Plaka:* {plaka}

📋 *Yapılan İşlemler:*
{items_formatted}
💵 *KDV Hariç:* {subtotal:,.2f} TL
🧾 *KDV (%20):* {vat:,.2f} TL
💰 *TOPLAM TUTAR:* *{total_price:,.2f} TL*

📄 *PDF Teklifiniz:*
{pdf_url}

📊 *Dükkan Yönetim Paneli:*
{dashboard_url}
----------------------------------------
💡 _Dijital Ustabaşı ile işiniz saniyeler içinde cebinizde!_"""

    send_result = send_whatsapp_message(clean_phone, response_msg)
    
    return {
        "success": True,
        "quote": saved_quote,
        "pdf_url": pdf_url,
        "whatsapp_message": response_msg,
        "send_result": send_result
    }
