import os
import re
import json
import urllib.request
import urllib.error
import base64
from dotenv import load_dotenv

try:
    from openai import OpenAI
except ImportError:
    pass

# Load env variables
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

def get_openai_api_key() -> str:
    """
    Retrieves the OpenAI API key (for backward compatibility).
    """
    try:
        from core.hr import ik_merkezi
        vault = ik_merkezi.get_worker("VaultService")
        if vault:
            key = vault.get_secret("openai_api_key") or vault.get_secret("OPENAI_API_KEY")
            if key:
                return key
    except Exception:
        pass
        
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.abspath(os.path.join(base_dir, "..", ".."))
        secrets_path = os.path.join(repo_root, "storage", "secrets.json")
        if os.path.exists(secrets_path):
            with open(secrets_path, "r", encoding="utf-8") as f:
                secrets = json.load(f)
                key = secrets.get("openai_api_key") or secrets.get("OPENAI_API_KEY")
                if key:
                    return key
    except Exception:
        pass
        
    return os.getenv("OPENAI_API_KEY") or ""


def get_gemini_api_key() -> str:
    """
    Retrieves the Gemini API key.
    First tries VaultService, then falls back to secrets.json, then env variables.
    """
    try:
        from core.hr import ik_merkezi
        vault = ik_merkezi.get_worker("VaultService")
        if vault:
            key = vault.get_secret("gemini_api_key") or vault.get_secret("google_api_key") or vault.get_secret("GEMINI_API_KEY")
            if key:
                return key
    except Exception:
        pass
        
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.abspath(os.path.join(base_dir, "..", ".."))
        secrets_path = os.path.join(repo_root, "storage", "secrets.json")
        if os.path.exists(secrets_path):
            with open(secrets_path, "r", encoding="utf-8") as f:
                secrets = json.load(f)
                key = secrets.get("gemini_api_key") or secrets.get("google_api_key") or secrets.get("GEMINI_API_KEY")
                if key:
                    return key
    except Exception:
        pass
        
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""


COMMON_BRANDS = [
    "fiat", "renault", "ford", "volkswagen", "vw", "opel", "toyota", "hyundai", 
    "peugeot", "honda", "citroen", "audi", "bmw", "mercedes", "nissan", "seat", 
    "skoda", "volvo", "dacia", "kia", "chevrolet", "mazda", "mitsubishi", "suzuki",
    "passat", "golf", "clio", "megane", "focus", "astra", "corolla", "egea", "polo",
    "linea", "symbol", "caddy", "transporter", "civic", "qashqai", "duster"
]

NUMBER_MAP = {
    "sıfır": 0, "bir": 1, "iki": 2, "üç": 3, "dört": 4, "beş": 5, "altı": 6, "yedi": 7, "sekiz": 8, "dokuz": 9,
    "on": 10, "yirmi": 20, "otuz": 30, "kırk": 40, "elli": 50, "altmış": 60, "yetmiş": 70, "seksen": 80, "doksan": 90,
    "yüz": 100, "bin": 1000, "milyon": 1000000
}

def transcribe_audio_gemini(audio_file_path: str, model_name: str, api_key: str) -> str:
    """
    Helper function to transcribe audio using a specific Gemini model via Google AI Studio API.
    """
    with open(audio_file_path, "rb") as audio_file:
        audio_data = audio_file.read()
        
    encoded_audio = base64.b64encode(audio_data).decode("utf-8")
    
    # Determine mime type based on file extension
    ext = os.path.splitext(audio_file_path)[1].lower()
    if ext == ".webm":
        mime_type = "audio/webm"
    elif ext == ".wav":
        mime_type = "audio/wav"
    elif ext in [".mp3", ".mpeg"]:
        mime_type = "audio/mp3"
    elif ext in [".ogg", ".oga"]:
        mime_type = "audio/ogg"
    elif ext in [".m4a", ".mp4"]:
        mime_type = "audio/m4a"
    else:
        mime_type = "audio/webm"  # fallback default

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    request_data = {
        "contents": [
            {
                "parts": [
                    {
                        "inlineData": {
                            "mimeType": mime_type,
                            "data": encoded_audio
                        }
                    },
                    {
                        "text": (
                            "Sen profesyonel bir oto tamir servisi dijital ustabaşısı ve ses deşifre uzmanısın. "
                            "Aşağıdaki ses kaydı sanayi ortamında, otomobil tamirhanesinde dükkan gürültüsü (kompresör, matkap, metal sesleri) altında kaydedilmiştir. "
                            "Arka plandaki sanayi gürültüsünden etkilenmeden konuşmacının Türkçe sözlerine odaklan. "
                            "Özellikle araç plakası (örn: 34 ABC 123 veya otuz dört abc yüz yirmi üç), araç modeli, yedek parça/tamir kalemleri (triger seti, fren balatası, filtre değişimi vb.) ve fiyat tutarlarına odaklanarak konuşulan sözleri eksiksiz ve doğru Türkçe ile metne dök. "
                            "Sadece konuşulan metni yaz, harici açıklama ekleme."
                        )
                    }
                ]
            }
        ]
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(request_data).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=30) as response:
        res_body = response.read().decode("utf-8")
        res_json = json.loads(res_body)
        candidates = res_json.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                text = parts[0].get("text", "").strip()
                if text:
                    return text
        raise Exception("Gemini API boş veya geçersiz yanıt döndürdü.")


# Global flag to track Whisper availability
IS_WHISPER_AVAILABLE = True

def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribes the given audio file using a cascading fallback approach:
    1. OpenAI Whisper (whisper-1) - if OpenAI API key is present and Whisper is active
    2. Google Gemini 3.5 Flash (gemini-3.5-flash) - if Gemini API key is present
    3. Google Gemini 3.1 Flash Lite (gemini-3.1-flash-lite) - if Gemini API key is present
    """
    global IS_WHISPER_AVAILABLE
    errors = []
    
    # 1. Try OpenAI Whisper
    openai_key = get_openai_api_key()
    if openai_key and IS_WHISPER_AVAILABLE:
        try:
            import httpx
            from openai import OpenAI
            client = OpenAI(api_key=openai_key, http_client=httpx.Client())
            with open(audio_file_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="tr",
                    prompt="Oto tamir servisi teklifi: 34 ABC 123 plaka, periyodik bakım, triger seti, fren balatası, yağ filtre değişimi, nakit fiyat."
                )
                if transcript and transcript.text:
                    return transcript.text.strip()
            raise Exception("Whisper boş deşifre döndürdü.")
        except Exception as e:
            errors.append(f"Whisper Hatası: {str(e)}")
            err_msg = str(e).lower()
            # If rate limit or quota exceeded, temporarily disable Whisper to speed up subsequent requests
            if "insufficient_quota" in err_msg or "rate limit" in err_msg or "429" in err_msg or "401" in err_msg:
                print(f"[Warning] Whisper permanent error caught ({str(e)}). Bypassing Whisper for subsequent requests to speed up transcription.")
                IS_WHISPER_AVAILABLE = False
            
    # 2. Try Gemini Models
    gemini_key = get_gemini_api_key()
    if gemini_key:
        for model in ["gemini-3.5-flash", "gemini-3.1-flash-lite"]:
            try:
                return transcribe_audio_gemini(audio_file_path, model, gemini_key)
            except Exception as e:
                errors.append(f"Gemini ({model}) Hatası: {str(e)}")
                
    # If all failed, raise ValueError
    if not errors:
        raise ValueError(
            "Ses deşifre API anahtarı (OpenAI veya Gemini) sistemde tanımlı değil. "
            "Lütfen .env veya secrets.json dosyasına anahtarınızı ekleyin."
        )
    error_summary = " | ".join(errors)
    raise ValueError(f"Ses deşifre edilemedi. Denenen tüm servisler başarısız oldu. Hatalar: {error_summary}")



def turkish_word_to_number(word_str: str) -> float:
    """
    Converts a Turkish written number (e.g. 'bin beş yüz', 'iki buçuk') to float/int.
    """
    words = word_str.lower().strip().split()
    total = 0
    current = 0
    
    # Handle "buçuk" (e.g. "iki buçuk" -> 2.5 or 2500, in sanayi "iki buçuk" usually means 2500 if context is thousands)
    # Let's check if "buçuk" is in words
    is_bucuk = False
    if "buçuk" in words:
        is_bucuk = True
        words.remove("buçuk")

    if not words and is_bucuk:
        return 500  # "buçuk" on its own (slang for 500)

    for word in words:
        if word in NUMBER_MAP:
            val = NUMBER_MAP[word]
            if val == 100:
                if current == 0:
                    current = 100
                else:
                    current *= 100
            elif val == 1000:
                if current == 0:
                    current = 1000
                else:
                    current *= 1000
                total += current
                current = 0
            elif val == 1000000:
                if current == 0:
                    current = 1000000
                else:
                    current *= 1000000
                total += current
                current = 0
            else:
                current += val
        # Check if it's a digit inside text
        elif word.isdigit():
            current += int(word)

    total += current

    if is_bucuk:
        # In Turkish auto repair:
        # If total is small (e.g. 1, 2, 5), "buçuk" means +500 (e.g., "iki buçuk" -> 2500, "bir buçuk" -> 1500, "yedi buçuk" -> 7500)
        # If total is 0, "buçuk" is 500.
        if total < 100:
            total = total * 1000 + 500
        else:
            total += 0.5  # literal 0.5 (fallback)
            
    return total

def rule_based_parser(text: str) -> dict:
    """
    Rule-based parser using regex and string matching to parse repair jobs, plate, and vehicle.
    """
    text_lower = text.lower()
    
    # 1. Extract Plaka
    # Turkish plate formats: 2 digits + 1-3 letters + 2-4 digits
    plate_pattern = r"\b(\d{2})\s*([a-z]{1,3})\s*(\d{2,4})\b"
    plate_match = re.search(plate_pattern, text_lower)
    plaka = ""
    if plate_match:
        plaka = f"{plate_match.group(1).upper()}{plate_match.group(2).upper()}{plate_match.group(3)}"
        # Remove plate from text to avoid parsing it as price/work
        text_lower = text_lower.replace(plate_match.group(0), "")
        
    # 2. Extract Vehicle Brand/Model
    vehicle = "Bilinmeyen Araç"
    for brand in COMMON_BRANDS:
        if brand in text_lower:
            vehicle = brand.title()
            # Try to grab the word after the brand as model (e.g., "Fiat Egea" or "Audi A4")
            words = text_lower.split()
            try:
                brand_idx = words.index(brand)
                if brand_idx + 1 < len(words):
                    next_word = words[brand_idx + 1]
                    # Make sure it's not a price or conjunction
                    if next_word not in ["ve", "lira", "tl", "bin", "buçuk", "değişimi", "bakımı"] and not next_word.isdigit():
                        vehicle = f"{vehicle} {next_word.title()}"
            except ValueError:
                pass
            break

    # 3. Extract Usta Notu (Foreman note)
    # Search for terms like "usta notu", "not olarak", "açıklama"
    usta_note = ""
    note_pattern = r"(?:usta notu|not olarak|not)\s*:?\s*(.*)$"
    note_match = re.search(note_pattern, text_lower)
    if note_match:
        usta_note = note_match.group(1).strip().capitalize()
        # Remove note from text for repair parsing
        text_lower = text_lower.split(note_match.group(0))[0]

    # 4. Extract Repair Items and Prices
    # Split text into segments by typical conjunctions/delimiters
    segments = re.split(r",| ve | ayrıca | artı | ile ", text_lower)
    items = []
    
    # Number extraction regex (matches digits or written turkish number words)
    number_words = "|".join(NUMBER_MAP.keys()) + "|buçuk"
    price_pattern = rf"(\d+[\d\s\.]*|\b(?:{number_words})(?:\s+(?:{number_words}))*\b)"
    
    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue
            
        # Find price in segment
        matches = re.findall(price_pattern, segment)
        if not matches:
            continue
            
        # We take the last match as the price usually (e.g., "yağ değişimi 1500 tl" -> "1500 tl" is the price)
        raw_price_str = matches[-1].strip()
        
        # Clean price string and evaluate
        price_val = 0
        cleaned_price = re.sub(r"lira|tl|liras|liralık", "", raw_price_str).strip()
        
        if cleaned_price.isdigit():
            price_val = float(cleaned_price)
        elif any(w in cleaned_price for w in NUMBER_MAP.keys()) or "buçuk" in cleaned_price:
            price_val = turkish_word_to_number(cleaned_price)
        else:
            # Maybe it has dots like "1.500" or spaces "1 500"
            clean_digits = re.sub(r"[\s\.]", "", cleaned_price)
            if clean_digits.isdigit():
                price_val = float(clean_digits)
                
        if price_val == 0:
            continue
            
        # Description is the segment with the price and currency words removed
        desc = segment.replace(raw_price_str, "")
        # Remove leftover currency words and extra whitespaces
        desc = re.sub(r"\b(lira|tl|liras|liralık|ve)\b", "", desc)
        
        # Clean brand/model from the description so it doesn't pollute the job name
        for brand in COMMON_BRANDS:
            desc = re.sub(rf"\b{brand}\b", "", desc, flags=re.IGNORECASE)
        if vehicle and vehicle != "Bilinmeyen Araç":
            for word in vehicle.split():
                desc = re.sub(rf"\b{word}\b", "", desc, flags=re.IGNORECASE)
                
        desc = re.sub(r"\s+", " ", desc).strip().capitalize()
        
        if desc:
            items.append({
                "description": desc,
                "price": price_val
            })

    # If no plaka could be found, return a default
    if not plaka:
        plaka = "PLAKASIZ"

    return {
        "plaka": plaka,
        "vehicle": vehicle,
        "items": items,
        "usta_note": usta_note
    }

def parse_repair_text(text: str) -> dict:
    """
    Parses Turkish repair text into structured JSON using Google AI Studio (Gemini 3.1 Flash Lite).
    Falls back to rule_based_parser if Gemini is unavailable or fails.
    """
    api_key = get_gemini_api_key()
    if not api_key:
        print("Gemini API key is not configured. Falling back to offline rule_based_parser.")
        return rule_based_parser(text)
        
    try:
        prompt = f"""
        Aşağıdaki Türkçe oto tamir ses döküm metninden bilgileri ayıkla ve JSON formatında döndür.
        Metin: "{text}"
        
        JSON Şeması:
        {{
            "plaka": "varsa plaka numarası (örn: 34ABC123), yoksa 'PLAKASIZ'",
            "vehicle": "varsa araç marka ve modeli (örn: Fiat Egea, Audi A4), yoksa 'Bilinmeyen Araç'",
            "items": [
                {{
                    "description": "yapılan iş veya parça adı (Türkçe ve düzgün yazımlı, örn: Ön fren balatası değişimi)",
                    "price": yapılan işin KDV hariç fiyatı (sayısal değer, örn: 1200)
                }}
            ],
            "usta_note": "varsa ustaya özel not veya açıklama (örn: Parçalar orijinal takıldı), yoksa boş string ''"
        }}
        
        Kurallar:
        - Türkçe sayı kelimelerini sayıya çevir (örn: 'bin beş yüz' -> 1500, 'iki buçuk' -> 2500, 'yedi buçuk' -> 7500).
        - Sanayi ağzını düzelt (örn: 'balata değişimi' -> 'Fren Balatası Değişimi').
        - KDV hesaplama, ham fiyatı yaz.
        - Yanıt olarak SADECE geçerli bir JSON döndür, açıklama veya markdown bloğu ekleme.
        """
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        request_data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json"
            }
        }
        
        req = urllib.request.Request(
            url, 
            data=json.dumps(request_data).encode("utf-8"), 
            headers=headers, 
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            candidates = res_json.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    result_text = parts[0].get("text", "").strip()
                    if result_text.startswith("```"):
                        result_text = re.sub(r"^```(?:json)?\n|```$", "", result_text, flags=re.MULTILINE).strip()
                    return json.loads(result_text)
            raise ValueError("Gemini API boş veya geçersiz yanıt döndürdü.")
            
    except Exception as e:
        print(f"Gemini API parse hatası: {str(e)}. Çevrimdışı kurallı ayrıştırıcıya geçiliyor...")
        return rule_based_parser(text)

