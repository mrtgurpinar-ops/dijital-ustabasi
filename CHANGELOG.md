# 📜 Dijital Ustabaşı - Geliştirme Günlüğü (Changelog)

Projedeki tüm majör revizyonlar, güvenlik güncellemeleri me yeni özellikler bu dosyada SemVer prensiplerine uygun olarak kayıt altına alınmaktadır.

## [v1.4.0] - 2026-08-02 (Oto Lastik & Jant Hizmetleri Entegrasyonu)

### 🛞 Oto Lastik & Jant Dükkan Desteği (`templates/index.html`)
- **Oto Lastik & Jant Hizmetleri:** Lastik Değişimi, Rot-Balans Ayarı ve Lastik Oteli Saklama Hizmetleri şablon kartları arayüze entegre edildi.
- **📱 Rol Butonlarında Telefon Numaraları:** Hızlı test giriş butonlarında 5 rolün telefon numaraları (`05555105635`, `05550000000`, `05553330003`, `05552220002`, `05551110001`) açık şekilde görüntülendi.

---

## [v1.3.0] - 2026-08-02 (Multi-Tenant PostgreSQL Mimarisi & Kod Temizliği)

### 🧹 Proje Temizliği ve Çok Kiracılı Mimari (`cloud_storage.py`, `models.py`, `railway.json`)
- **🧹 Yuvalanmış Klasör Temizliği:** Hatalı oluşan `projects/dijital_ustabasi/projects` dizin hiyerarşisi tamamen kaldırıldı.
- **⚡ Import İthalat Sadeleştirmesi (`main.py`, `cloud_storage.py`, `models.py`):** Karmaşık `try...except ModuleNotFoundError` ikili ithalat yapıları sökülerek saf modüler importlara dönüştürüldü.
- **🌐 Dockerfile Builder Sabitlemesi (`railway.json`):** Railway derleme süreci `"builder": "DOCKERFILE"` olarak sabitlendi.
- **🗄️ Multi-Tenant B2B2C Veri İzolasyonu:** `shop_id` yabancı anahtarları ile dükkanlar ve onların müşterileri tam veri izolasyonuna kavuşturuldu.

---

## [v1.2.2] - 2026-08-02 (PostgreSQL Docker Compose & Temiz Şema Yapılandırması)

### 🐘 Yerel ve Canlı PostgreSQL Şema Altyapısı (`docker-compose.yml`, `requirements.txt`, `database.py`)
- **Yerel PostgreSQL & Adminer Masası (`docker-compose.yml`):** PostgreSQL 16 veritabanı motoru (`localhost:5432`) ve Adminer Web veritabanı paneli (`http://localhost:8081`) eklendi.
- **Eski Test Verileri Temizliği:** Eski test verileri taşınmayacak şekilde temiz şema yapılandırıldı. 5 hazır rol hesabı (`👑 Admin`, `⏳ Deneme`, `⭐️ Usta`, `🛠️ Kalfa`, `👶 Çırak`) doğrudan veritabanında başlatıldı.

---

## [v1.2.1] - 2026-08-02 (PostgreSQL psycopg2-binary ve pg8000 Sürücülerinin Eklenmesi)

### 🗄️ PostgreSQL Sürücü Entegrasyonu (`requirements.txt`, `database.py`)
- **PostgreSQL Sürücüleri (`requirements.txt`):** Python ve SQLAlchemy'nin PostgreSQL sunucularıyla haberleşmesini sağlayan `psycopg2-binary>=2.9.9` ve `pg8000>=1.30.5` bağımlılıkları eklendi.
- **Otomatik Sürücü Çözümleme (`database.py`):** `DATABASE_URL` okunduğunda varsayılan PostgreSQL sürücüsüne ek olarak `pg8000` yedekli bağlantı katmanı entegre edildi.

---

## [v1.2.0] - 2026-08-02 (5 Katmanlı Rol Yapısı & Araç Parkı CRM Mimarisi)

### 👥 5 Katmanlı Rol Mimarisi (`cloud_storage.py`, `main.py`, `templates/index.html`)
- **5 Hazır Test Hesabı (`cloud_storage.py`):** Veritabanı başlatıldığında Admin (`05555105635`), Deneme (`05550000000`), Usta (`05553330003`), Kalfa (`05552220002`) ve Çırak (`05551110001`) varsayılan olarak otomatik tanımlandı.
- **⚡ Hızlı Rol Giriş Butonları (`templates/index.html`):** Giriş ekranına 5 rol için tek tıkla otomatik doldurup giriş yapmayı sağlayan test düğmeleri eklendi.
- **🚗 Araç Parkı CRM Uç Noktası (`main.py`):** Plakaya göre tüm servis geçmişi ve toplam harcamayı sunan `GET /api/vehicle/crm/{plaka}` API uç noktası eklendi.

---

## [v1.1.1] - 2026-08-02 (Süper Admin Giriş & Entegre Yönetim Masası)

### 👑 Süper Admin Hesabı & Entegre Yönetim Yetkisi (`cloud_storage.py`, `main.py`, `templates/index.html`)
- **Özel Admin Hesabı Entegrasyonu (`cloud_storage.py`):** `5555105635` telefon numarası ve `DijitalAdmin2026!` şifresi ile otomatik varsayılan Süper Admin dükkanı tanımlandı.
- **Sınırsız Yetki & Kilit Kaldırma (`main.py`, `templates/index.html`):** Admin girişi yapıldığında tüm paket kilitleri, deneme süresi sınırlamaları ve arşiv kısıtlamaları kaldırıldı (`is_admin: True`).
- **Entegre Dükkan Yönetim Masası (`templates/index.html`):** Çalışma alanı başlığında `👑 SÜPER ADMİN` rozeti ve üst kısımda dükkan listeleme, paket yükseltme, +30 gün uzatma, askıya alma ve silme işlevlerini sunan canlı yönetim masası açıldı.

---

## [v1.1.0] - 2026-08-02 (PostgreSQL İlişkisel Veritabanı & SaaS Mimarisi)

### 🗄️ Kurumsal PostgreSQL & SQLAlchemy ORM Altyapısı (`database.py`, `models.py`, `migrate_json_to_postgres.py`)
- **SQLAlchemy 2.0 ORM Entegrasyonu (`database.py`, `models.py`):** Yerel JSON dosyası yerine ilişkisel `ShopModel`, `CustomerModel`, `VehicleModel` ve `QuoteModel` veritabanı tabloları kuruldu.
- **Railway PostgreSQL Uyumluğu:** Railway platformu `DATABASE_URL` (`postgres://` -> `postgresql://`) otomatik algılama ve canlı veritabanı bağlantı motoru eklendi; yerelde SQLite fallback sağlandı.
- **Sıfır Veri Kaybı Aktarım Betiği (`migrate_json_to_postgres.py`):** Mevcut `database.json` dosyasındaki 2 dükkan ve 58 teklif kaydı otomatik olarak veritabanı tablolarına aktarıldı (Migrated 2 shops and 58 quotes).
- **Servis Katmanı Güncellemesi (`cloud_storage.py`):** `CloudStorage` arka planda SQLAlchemy ORM sorguları çalıştıracak ve JSON dosyasını yedekli tutacak şekilde yenilendi.

---

## [v1.0.11] - 2026-08-02 (Telefon + Şifre ile Güvenli Kimlik Doğrulama Sistemi)

### 🔑 Telefon + Şifre (Password) Auth Mimarisi (`cloud_storage.py`, `main.py`, `index.html`)
- **Güvenli Şifre Hashing (`cloud_storage.py`):** Şifre saklama için `hashlib.sha256` SHA-256 özeti algoritması entegre edildi. Dükkan veri yapısına `password_hash` alanı eklendi.
- **Eski Veri Uyumluğu (Backward Compatibility):** Mevcut dükkan verileri korunarak şifresi henüz olmayan eski dükkanların ilk girişinde şifre tanımlaması otomatik sağlandı.
- **Yeni Giriş & Kayıt Uç Noktaları (`main.py`):** `POST /api/shop/login`, `POST /api/shop/register` ve `POST /api/shop/change_password` API uç noktaları eklendi. Şifre en az 4 karakter şartına bağlandı.
- **Arayüz Şifre Göster/Gizle Butonu (`templates/index.html`):** Dükkan giriş kapısına (Auth Gate) şifre input'u ve göz ikonu ile dinamik göster/gizle ikonu yerleştirildi.

---

## [v1.0.10] - 2026-08-02 (Backend Refactoring & UI/UX Atıl Kod Temizliği)

### 🧹 Backend & UI/UX Kapsamlı Temizlik (`cloud_storage.py`, `main.py`, `parser.py`, `index.html`)
- **İplik Güvenliği (Thread Safety - `cloud_storage.py`):** `CloudStorage` veritabanı okuma ve yazma işlemlerine `threading.Lock()` eklenerek eşzamanlı isteklerde `database.json` veri kaybı riski engellendi.
- **Dükkan Telefon Zorunluluğu (`main.py`):** Metin ve ses simülasyonlarında telefon girilmediğinde sahte `5321234567` kaydı oluşturma mantık hatası giderildi; telefon girişi zorunlu kılındı.
- **Standart API Yanıt Yapısı (`main.py`):** `/api/quotes` uç noktası parametresiz çağrılarda da tutarlı `{success: True, total_quotes: ..., active_plates: ..., quotes: [...]}` dict yapısı dönecek şekilde güncellendi.
- **Gemini Model Güncellemesi & Ölü Kod Temizliği (`parser.py`):** Standart dışı `gemini-3.5-flash` model tanımları güncel `gemini-2.0-flash` ve `gemini-1.5-flash` modelleri ile değiştirildi. Monorepo dışı `core.hr.ik_merkezi` ölü import blokları temizlendi.
- **Atıl Şablon Silme (`templates/dashboard.html`):** Rotaların tamamı `index.html` Single Page App yapısına bağlı olduğu için 79 KB'lık atıl `dashboard.html` şablonu projeden kaldırıldı.
- **Dinamik Rozet & Şablon Önbellek Yenileme (`index.html`, `admin.html`):** Sayfa açılışında dükkan paketi ve kimliğinin güncellenmesi sağlandı; CSS sürüm parametresi `?v=1.0.6` olarak güncellendi.

---

## [v1.0.9] - 2026-08-02 (Railway Kök Neden Düzeltmesi & Çift Dockerfile Mimarisi)

### 🚀 Railway 6 Maddelik Kök Neden Çözümü (`Dockerfile`, `nixpacks.toml`, `main.py`, `railway.json`)
- **`$PORT` String Parse Çakışma Çözümü (GÜNCELLEME):** Railway derleme loglarında tespit edilen `Error: Invalid value for '--port': '$PORT' is not a valid integer` hatası giderildi. Komutlar `python main.py` olarak değiştirilip `main.py` sonuna `if __name__ == '__main__':` bloğu eklendi. `$PORT` doğrudan Python `os.environ.get("PORT")` tarafından tam sayı (`int`) olarak okunması garanti edildi.
- **`package.json` vs Nixpacks Çakışma Çözümü:** Projedeki Capacitor `package.json` dosyasından ötürü Nixpacks'in projeyi Node.js sanması engellendi; `nixpacks.toml` ile `providers = ["python"]` zorunlu kılındı.
- **FastAPI Mount Çökme Engeli:** `main.py` içinde `app.mount("/data", StaticFiles(directory=STORAGE_DIR))` öncesine `os.makedirs(STORAGE_DIR, exist_ok=True)` eklenerek taze konteyner çökmesi %100 önlendi.
- **Monorepo `sys.path` Çözümü:** `MONOREPO_ROOT` `sys.path`'e eklenerek `antigravity_core` dizininden başlatmada `ModuleNotFoundError` çözüldü.
- **Çift Dockerfile Mimarisi:** Hem monorepo root hem sub-repo root için `Dockerfile` ve `Procfile` `python main.py` ile güncellendi.
- **Railway API Token Entegrasyonu:** Token (`204d293c-dfb4-4988-8492-aa6a206db8fc`) ve canlı domain (`dijital-ustabasi-production-7fe5.up.railway.app`) `railway_api.py` betiğine bağlandı.


---

## [v1.0.8] - 2026-08-02 (Railway Sıfırdan Canlıya Alma & Yapılandırma Senkronizasyonu)

### 🚀 Railway Re-deployment & Tam Bağımsız Yapılandırma (`railway.json`, `Procfile`, `mise.toml`)
- **Sıfırdan Canlıya Alma Hazırlığı:** Railway platformunda sıfırlanan `dijital-ustabasi` projesi için alt dizin ve bağımsız repozitör canlıya alma yapılandırmaları tam uyumlu hale getirildi.
- **Port ve Başlatma Komutu Senkronizasyonu:** `uvicorn main:app --host 0.0.0.0 --port $PORT` başlatma komutu, `mise.toml` imza koruması (`python.github_attestations = false`) ve Python 3.11.9 sürüm sabitlemesi doğrulandı.
- **Çift Yönlü Git Senkronizasyonu:** `mrtgurpinar-ops/dijital-ustabasi` bağımsız reposu ve `antigravity_core` ana reposu ile canlıya alma push işlemi sağlandı.

---

## [v1.0.7] - 2026-07-27 (Railway Monorepo Çakışma Düzeltmesi & Bağımsız Yapılandırma)

### 🛠️ Railway Deployment & Nixpacks Çakışma Çözümü (`railway.json`, `projects/dijital_ustabasi/railway.json`)
- **Kök Dizin Start Command Düzeltmesi:** Kök `railway.json` dosyasındaki yanlış VoltNet uvicorn hedefi düzeltilerek `uvicorn projects.dijital_ustabasi.main:app --host 0.0.0.0 --port $PORT` ve sağlık yolu `/` yapıldı. HTTP 502 Bad Gateway hatası giderildi.
- **Bağımsız Yapılandırma Desteği:** `projects/dijital_ustabasi/railway.json` oluşturularak projenin alt dizinden bağımsız root directory canlıya alma uyumluluğu sağlandı.

---

## [v1.0.6] - 2026-07-27 (Remotion 10 Saniyelik Tanıtım Videosu & Medya Varlıkları)

### 🎬 Remotion Video Tanıtım Altyapısı (`c:\Users\MSI-NB\OneDrive\Desktop\Remotion`)
- **10 Saniyelik Full HD Tanıtım Videosu:** React & Remotion kütüphaneleri kullanılarak kod tabanlı 300 karelik (30 FPS) 1080p tanıtım MP4 videosu oluşturuldu ve render edildi (`out/dijital_ustabasi_promo.mp4`).
- **Sahne Kurgusu:**
  1. *Ses Kaydı & AI Dönüşümü:* WhatsApp sesli mesajlarını dinleyip AI ile okuyan animasyonlu ses dalgaları.
  2. *Otomatik Parça Ayrıştırma & PDF:* Fiyatlandırma sayacı (`₺0` -> `₺9.200`) ve 3D görünümlü cam (glassmorphism) PDF teklif kartı.
  3. *Brand & CTA:* Parlayan logo efekti ve 7 Gün Ücretsiz Deneme çağrı butonu.

---

## [v1.0.5] - 2026-07-26 (Görsel Aksiyon Şeridi, Admin Panel Merkezli Döngü & Bitiş Tarihi Yönetimi)

### 👑 Admin Panel Merkezli Dükkan Yaşam Döngüsü (`cloud_storage.py`, `main.py`, `templates/index.html`)
- **Admin Üstün Yetki Hiyerarşisi:** Deneme süresi başlayan dükkanlar admin paneline doğrudan `package='usta'` olarak kaydolur. Yönetici bir dükkanı `Çırak`, `Kalfa` veya `Usta` yaptığında yönetici kararı üstün yetki olarak tüm deneme sürelerini ezer ve anında ilgili paket sınırlarını uygular.
- **Otomatik Süre Dolumu & Askı:** Deneme/paket süresi dolduğunda (`expires_at`) sistem dükkanı otomatik olarak askıya alır (`is_active=False`) ve erişimi kilitler.

### 🗓️ Yönetici Masası Bitiş Tarihi & Süre Uzatma (`templates/admin.html`)
- **Tarih Seçici (`<input type="date">`):** Yönetici paneline her dükkan için özel bitiş tarihi seçebileceği takvim alanı eklendi.
- **Hızlı Uzatma Butonları (`+7g`, `+30g`):** Yönetici panelinden tek tıkla süresine +7 veya +30 gün eklenebilmesi sağlandı.

### 📄 PDF İndirme & Uzantı Düzeltmesi (`main.py`, `templates/index.html`)
- **Çift Başlık (Duplicate Content-Disposition) Düzeltmesi:** FastAPI `FileResponse` yanıtındaki yinelenen başlık hatası giderildi, tekil `Content-Disposition` başlığı ve `.pdf` uzantısı garanti altına alındı. Mobil ve masaüstü tarayıcılarda PDF dosyalarının doğrudan `.pdf` uzantısıyla inmesi sağlandı.

---

## [v1.0.4] - 2026-07-26 (Sürdürülebilir Ses & Teklif Ayrışımı, Tam Askıya Alma Kilidi, Admin Tek Tek Silme X Butonu)

### 🎙️ Sürdürülebilir Ses & Teklif Ayrıştırması (`main.py`, `templates/index.html`)
- **Deşifre & Üretim Ayrımı (`POST /api/voice/transcribe`):** Sesli kayıt bittiğinde ses SADECE METNE DÖKÜLÜR (0 teklif kaydeder). Teklif üretimi Ustabaşının `Teklif Üret` butonuna basmasıyla SADECE 1 KEZ gerçekleşir.
- **İstemcide `quote_id` Tekilleştirmesi:** Arayüzde teklifler basılmadan önce `quote_id` bazında süzülerek çoklama tamamen engellenmiştir.

### ⛔ Tam Askıya Alma Kilidi (`main.py`, `templates/index.html`)
- **Tüm Özelliklerin Engeli:** Askıya alınan dükkanların TÜM API uç noktaları HTTP 403 Forbidden döner. İstemcide tam ekran uyarı mesajı görüntülenir: `"Hesabınız askıya alınmıştır, lütfen yönetici ile iletişime geçin."`

### 🛠️ Yönetici Masası (Admin Panel) Entegrasyonları (`templates/admin.html`, `main.py`)
- **Kayıt Tarihi & 7 Gün Hesabı:** Yönetici tablosuna dükkanın **Kayıt Tarihi** eklendi ve 7 günlük deneme süresi `created_at` tarihinden itibaren hesaplandı.
- **Tek Tek Dükkan Silme (`🗑️ Sil (X)`):** Her dükkan satırına kırmızı sil butonu eklendi.
- **Tüm Verileri Sıfırla:** Yönetici Paneli başlığına tüm Railway kalıcı test verilerini sıfırlayan buton eklendi.

---

## [v1.0.3] - 2026-07-26 (Kesin Giriş Duvarı Mimarisi, Paket Seçim & Talep Akışı, Çoklama İzolasyonu)

### 🔒 Kesin Giriş Duvarı & Kimlik Doğrulama (`#authLandingView`, `templates/index.html`)
- **Sıfır Sızıntı Giriş Duvarı:** Giriş yapılmadığı veya 7 günlük deneme başlatılmadığı sürece Çalışma Alanı (Teklif Motoru, İstatistikler, Arşiv) **TAMAMEN GİZLİ (`display: none;`)** kılınmıştır.
- **Seçilebilir Paket Kartları & 05XX Numerik Giriş:** Karşılama alanında tıklanabilir Çırak, Kalfa, Usta kartları ve 05 ile başlayan numerik telefon alanı entegre edilmiştir.
- **Kayıtsız Numara Kontrolü & Paket Talep Akışı:** Numarasını girip Giriş Yap butonuna basan kayıtsız kullanıcılara `"Numara bulunamadı!"` uyarısı verilerek seçtiği paket için **`Paket Talep Et`** (Yönetici onayına gönder) butonu sunulmuştur.
- **7 Günlük Ücretsiz Deneme:** Tek tıkla 7 günlük USTA paket denemesi başlatarak çalışma alanını açma imkanı sağlanmıştır.

### ⚡ Çoklama Engelleyici İzolasyon & Veri Temizliği (`cloud_storage.py`, `database.json`)
- Tekliflerin çift tetiklenmesi tamamen engellenmiş, veritabanı sıfırlanmıştır.

---

## [v1.0.2] - 2026-07-26 (Misafir Teklif Deneme & 7 Günlük Deneme ile PDF Açma Kurgusu)

### 🎤 Misafir Teklif Oluşturma (Guest Mode) (`templates/index.html`, `main.py`)
- **1 Adet Ücretsiz Deneme Teklifi:** Giriş yapmamış veya numara girmemiş ziyaretçiler karşılama ekranında 1 adet deneme teklifini sesli/yazılı olarak serbestçe oluşturabilir.
- **🔒 PDF Erişim Kilidi (`trialUnlockModal`):** Üretilen PDF teklifinin Önizle veya İndir butonuna tıklandığında "📄 Kurumsal PDF Teklifiniz Hazır! Görüntülemek için 7 gün denemeyi başlatın" kilit modalı açılır.
- **🚀 1-Tıkla Deneme & PDF Açılışı (`/api/quote/assign_phone`):** Ziyaretçi numarasını girdiği anda 7 günlük USTA denemesi başlar, teklif dükkanına bağlanır ve PDF belgesi anında ekranda önizlenir/indirilir.

---

## [v1.0.1] - 2026-07-26 (Mobil Arayüz Düzeltmeleri, Çakışmasız Butonlar, Karşılama Ekranı & Veri Sıfırlama)

### 📱 Mobil Uyum & Çakışmasız Aksiyon Butonları (`style.css`, `templates/index.html`)
- **Esnek Mobil Kart Yapısı (`.quote-card`):** Teklif kartları mobil cihazlarda esnek dikey kolon, masaüstünde geniş grid düzenine geçirildi.
- **Çakışmasız Butonlar (`.card-actions`):** `[✅ Onayla]`, `[❌ Reddet]`, `[👁️ Önizle]`, `[İndir]` butonlarının yazıları ve ikonları arasındaki çakışma tamamen çözüldü.
- **Esnek Sayfa Kaydırması (`style.css`):** Sayfayı kısıtlayan `100vh overflow:hidden` kuralı kaldırılarak mobil ve masaüstünde rahat, ferah kaydırma alanı sağlandı.

### 🏁 İlk Karşılama Ekranı & Deneme Başlatma Kutusu (`templates/index.html`)
- **Paket Kartları Hero Alanı:** Sayfanın en üstüne Çırak, Kalfa ve Usta esnaf paketlerini içeren Karşılama Ekranı yerleştirildi.
- **7 Günlük Deneme Giriş Kutusu:** Paketlerin hemen altında telefon numarası girilerek 7 Günlük Denemeyi tek tıkla başlatan giriş kutusu entegre edildi.

### 🧹 Veritabanı Sıfırlama (`storage/database.json`)
- Test sürecinin sıfırdan ve temiz yapılabilmesi için tüm dükkan ve teklif verileri temizlendi.

---

## [v1.0.0] - 2026-07-26 (Sıfırdan Tek Sayfa Bütünleşik Mimarı & Web/Mobil Odaklı Platform)

### 🚀 Tek Sayfa Bütünleşik Platform Mimarisi (`index.html`)
- **Bütünleşik Ana Sayfa:** Tüm geçmiş yönlendirme karmaşaları kaldırılarak siteye girildiği ilk anda **🎤 Canlı Sesli & Yazılı Teklif Motoru**, **📊 Canlı İstatistik Masası** ve **📋 Filtreli Teklif Arşivi** aynı ana ekranda buluşturuldu.
- **Filtreli Teklif Arşivi Sekmeleri:** `[Tüm Teklifler]`, `[Bekleyenler ⏳]`, `[Onaylananlar ✅]`, `[Reddedilenler ❌]` sekmeleri eklenerek müşteri bazlı onay/ret durum takibi sağlandı.

### 📦 Kesin Paket Yetki Kuralları (`main.py`, `cloud_storage.py`)
- **7 Günlük Ücretsiz Deneme Süresi:** Denemedeki tüm yeni kullanıcılara **USTA Paketinin TÜM ÖZELLİKLERİ** (Sınırsız arşiv, ciro analitiği, teklif üretici, logo yükleme) tanımlandı.
- **Çırak Paketi:** Sesten & Yazılı teklif oluşturma aktif, arşiv kilitli, Logo & Dükkan ismi değiştirme açık.
- **Kalfa Paketi:** Sesten & Yazılı teklif oluşturma aktif, **son 15 teklif arşivi** açık, Logo & Dükkan ismi değiştirme açık.
- **Usta Paketi:** Sınırsız arşiv + Ciro masası + Tüm özellikler açık.
- **Logo Yükleme & Dükkan İsmi:** Tüm paketlerde açık kılınarak paket karşılaştırma kartlarında net gösterildi.

### 🚫 WhatsApp Bağımsızlığı & Web/Mobil Odaklı Yapı
- WhatsApp bağımlılığı kaldırılarak sistem tamamen Web & Mobil (PWA) arayüzü üzerinden bağımsız ve kesintisiz kılındı.

### 🧪 Otomatik Test Paketi (`test_dijital_ustabasi.py`)
- Tüm v1.0.0 paket yetki ve arşiv sınırlarını doğrulayan 12 birim testi %100 başarıyla geçti.

---

## [v4.75.0] - 2026-07-26 (Deneme Süresi Paket Uyumluluğu, Sayaç Düzeltmeleri & Kalfa Arşiv Erişimi)

### 🐛 Deneme Süresi Paket Uyumluluğu & Teklif Arşivi Erişimi (`main.py`, `dashboard.html`)
- **Çırak Deneme Süresi Teklif Arşivi Erişimi (`main.py` -> `/api/quotes`):** 7 günlük aktif deneme süresinde (`is_in_trial = True`) olan Çırak paketindeki dükkanların teklif arşivine erişimi açıldı (`visible_quotes = all_quotes[:30]`). Deneme süresinde vaat edilen tam sürüm / arşiv deneme imkanı eksiksiz kılındı.
- **Kilit Ekranı (Lock Overlay) Güncellemesi (`dashboard.html`):** Aktif deneme süresince teklif arşivi üzerindeki bulanıklık ve kilit katmanı kaldırıldı; deneme süresi dolduğunda üye olma kilit ekranı devreye girecek şekilde yapılandırıldı.
- **Şeffaf Paket Durum Gösterimi (`dashboard.html` -> `updateShopIdentityUI`):** Header başlığında kullanıcının aktif paketi ve kalan deneme günü şeffaf olarak görüntülendi (`ÇIRAK (DENEME SÜRESİ - X GÜN KALDI)`).

### 📊 Statik Mock Verilerin Temizlenmesi & Sayaç Senkronizasyonu (`templates/dashboard.html`)
- **Statik Sahte Kartların Kaldırılması:** `dashboard.html` içerisinde ilk açılışta görünen statik sahte teklif kartları (`34 ABC 123` ve `06 XYZ 987`) ve varsayılan 120/84 sahte istatistik sayıları kaldırıldı.
- **Gerçek Zamanlı Sayaçlar:** Sayfa yüklendiğinde sayaçların doğrudan veritabanından gelen gerçek teklif ve kayıtlı araç sayılarıyla başlaması sağlandı. 1 teklif eklendiğinde sayacın 3'e veya 5'e sıçraması engellendi.

### 🧪 Otomatik Test Doğrulaması (`test_dijital_ustabasi.py`)
- Tüm birim testleri (14/14 test) başarıyla çalıştırıldı ve %100 doğrulandı.

---

## [v4.74.0] - 2026-07-26 (Kapsamlı Kod & Canlı Ortam Denetimi, WhatsApp Bot Sesli Mesaj & Nakit İndirim Düzeltmesi)

### 🐛 WhatsApp Bot Sesli Mesaj İşleme & Nakit İndirimi Düzeltmesi (`whatsapp_bot.py`)
- **Ses Dosyası Temp Handling:** Meta WhatsApp Webhook üzerinden gelen ses kaydı byte'larının `transcribe_audio` fonksiyonuna gönderilmeden önce geçici `temp/` dizinine dosya olarak yazılması ve `finally` bloğu ile temizlenmesi sağlandı. Sesli mesaj işleme çökmesi (`TypeError: transcribe_audio() takes 1 positional argument but 2 were given`) tamamen giderildi.
- **Nakit Ödeme İndirimi Senkronizasyonu:** `whatsapp_bot.py` üzerinden oluşturulan teklif veritabanı kayıtlarına `%10` nakit indirimi hesabı (`discount_price = total_price * 0.90`) eklendi.
- **Unicode Safe Logging:** Konsol loglamalarında emoji ve UTF-8 karakter koruması güçlendirildi.

### 🛡️ Statik Data Mount & Uyum (`main.py`)
- **`/data` Static Route:** Backend üzerinde `/data` statik mount'u eklenerek preview/fallback statik veri sunum kuralları tamamlandı.

### 🧪 Otomatik Birim Testi Genişletmesi (`test_dijital_ustabasi.py`)
- WhatsApp Bot sesli/yazılı mesaj işleme ve indirim hesaplama mantığını doğrulayan 14. otomatik unittest eklendi (14/14 test %100 başarılı).

### 🚀 Önbellek Güncellemesi (Cache Busting)
- `index.html`, `dashboard.html` ve `admin.html` şablonlarındaki CSS parametresi `?v=4.74.0` olarak güncellendi.

---

## [v3.16.0] - 2026-07-26 (Çift Katmanlı Kalıcı Önbellek Mimarisi & Teklif Masası Saklaması)

### 💾 Çift Katmanlı Önbellek & Kalıcı Saklama (`templates/dashboard.html`)
- **Instant LocalStorage Loading (`loadQuotes` & `renderQuotesListUI`):** Teklifler üretildiğinde ve sunucudan çekildiğinde `cached_quotes_${phone}` anahtarıyla tarayıcının yerel hafızasına yedeklendi. Sayfa yenilendiğinde (`F5`) veya bağlantı dalgalanmasında teklifler anında `localStorage` üzerinden ekrana basıldı, ardından sunucuyla tam senkronize edildi.
- **Kesintisiz Saklama:** Teklif Masasında üretilen tekliflerin silinmesi veya sayfa yenilenince kaybolması engellendi.
- **Cache Busting (`?v=4.73.0`):** Önbellek sürümü yükseltildi.

---

### 🛡️ Backend Paket Muafiyeti (`main.py` -> `check_shop_access`)
- **Deneme Süresi Sınırının Çırak Paketi İle Sınırlandırılması:** `check_shop_access(shop)` fonksiyonunda 7 günlük ücretsiz deneme süresi engeli YALNIZCA `package: "cirak"` için geçerli kılındı. Kalfa ve Usta paketine geçen dükkanlar deneme süresi engelinden %100 muaf tutuldu.

### 🎨 Tip Korumalı Rendering & Format Güvenliği (`templates/dashboard.html`)
- **Defansif `quotes.map` Rendering:** `total_price`, `discount_price`, `plaka`, `vehicle`, `pdf_filename` ve `created_at` dönüşümleri tip korumalı hale getirildi. Veritabanındaki bir alanda eksik/tanımsız veri olsa dahi JavaScript `TypeError` vermeden teklif kartları ekrana eksiksiz basıldı.
- **Frontend Kilit Katmanı Güncellemesi (`updateUIForPackage`):** `daysLeft <= 0` kilit katmanının yalnızca Çırak paketi dükkanlarında devreye girmesi sağlandı, Kalfa/Usta üyelerde teklif listesi anında açıldı.
- **Cache Busting (`?v=4.72.0`):** Önbellek sürümü yükseltildi.

---

### 📞 Esnek Telefon Eşleme & DB Migrasyonu (`cloud_storage.py`)
- **Telefon Format Normalizasyonu (`get_quotes`):** Teklif listesi sorgulanırken `normalize_phone(q["phone_number"]) == normalize_phone(phone_number)` esnek eşleşmesi uygulandı. Telefon numarası `05555555555`, `+905555555555` veya `5555555555` formatında kaydedilmiş olsa dahi Kalfa ve Usta paketindeki dükkanların geçmiş tekliflerini %100 eksiksiz görüntülemesi sağlandı.
- **Otomatik DB Migrasyonu (`_migrate_db`):** Veritabanı başlangıcında kayıtlı tüm tekliflerin `phone_number` alanları otomatik 10 haneli standart formata (`5555555555`) dönüştürüldü.
- **Yeni Birim Testi (`test_kalfa_package_flexible_phone_quote_matching`):** Farklı telefon formatlarında kaydedilen tekliflerin Kalfa paketinde eksiksiz getirildiğini doğrulayan 13. otomatik birim testi eklendi (13/13 test %100 başarılı).
- **Cache Busting (`?v=4.71.0`):** Önbellek sürümü yükseltildi.

---

### 🎤 Sesli Metin Önizlemesi & Yazı Kutusuna Aktarma (`templates/dashboard.html`)
- **Speech-to-Text Prefill:** Mikrofona basıp konuşulduğunda ses metni (`transcription`) doğrudan ekrandaki **yazı kutusuna (`#chatMessage`)** döküldü. Esnaf ne söylendiğini kontrol edip gerekirse düzelttikten sonra `[Teklif Üret]` butonuna basarak onaylı PDF üretimi sağlandı.

### 📱 Mobil Uyumlu PDF Önizleme Modalı (`previewPdf`)
- **Otomatik Sekme Açmanın Kaldırılması:** `sendDirectTextMessage` sonrası zoraki `window.open` kaldırılarak mobil ve masaüstü uyumlu `previewPdf` modalı (`pdfModal`) açıldı. Esnaf modal üzerinden *"👁️ Teklifi Önizle"* ve *"📥 Cihaza İndir (PDF)"* seçeneklerini özgürce kullanabilir hale getirildi.

### 📊 İstatistik Kartları Düzeltmesi (`main.py`, `templates/dashboard.html`)
- **Gerçek Sayaç Verisi:** `GET /api/quotes` uç noktasına `total_quotes` ve `active_plates` sayısal özetleri eklendi. Çırak paketinde teklif listesi kilitli (`[]`) olsa dahi Toplam Teklif ve Kayıtlı Araç sayaçlarının 0 görünmesi engellendi, dükkanın gerçek sayıları gösterildi.
- **Cache Busting (`?v=4.70.0`):** Önbellek sürümü yükseltildi.

---

### 👑 Yönetici Paneli Senkronizasyonu & Backend Yetki Filtresi (`main.py`, `templates/admin.html`)
- **Backend Paket Sınırı (`GET /api/quotes`):** Dükkan paketi `cirak` ise teklif arşivi verileri API düzeyinde kilitlendi (`[]`), `kalfa` paketinde ilk 30 teklif sunuldu, `usta` paketinde sınırsız erişim verildi.
- **Dükkan Ekranı Kilit Entegrasyonu (`templates/dashboard.html`):** `loadQuotes()` akışında her zaman en güncel dükkan paketi çekilerek `updateUIForPackage(shop)` çalıştırıldı.
- **Çırak Paketi Teklif Arşivi Kilidi (`#quotesLockOverlay`):** Çırak statüsündeki dükkanların (Örn: MG Oto Servis) Kalfa alanı olan Geçmiş Teklif Arşivini görmesi engellendi; üzerine *"🔒 Teklif Arşivi Kalfa & Usta Paketine Özeldir"* kilit katmanı ve Kalfa yükseltme butonu yerleştirildi.
- **Cache Busting (`?v=4.69.0`):** Sürüm yükseltildi.

---

### 🔒 Varsayılan Paket & Kilit Mimarisi (`cloud_storage.py`, `templates/dashboard.html`)
- **Çırak Paketi Varsayılanı (`create_shop`):** Yeni kaydolan/denemeyi başlatan dükkanlara varsayılan olarak `package: "cirak"` atandı.
- **Kilitli Ciro Kartı (`locked-card`):** Çırak ve Kalfa paketlerinde Ciro Kartı üzerinde **"🔒 Usta Özel"** kilidi aktif kılındı (`ciroLock.style.display = "flex"`).
- **Kilit & Paket Modalı Bağlantısı:** Kilide tıklandığında doğrudan Paket Karşılaştırma ve Yönetici Uyarısı Modalı (`upgradeComparisonModal`) açılarak talep oluşturulması ve yöneticiyle iletişime geçilmesi sağlandı.

### 🧪 Otomatik HTML/JS Sentaks Testi (`test_dijital_ustabasi.py`)
- **`test_html_templates_js_syntax_validation`:** HTML şablonlarındaki tüm `<script>` bloklarını ayrıştıran ve unclosed `try {` veya kırık parantez hatalarını otomatik yakalayarak derleme/test aşamasında engelleyen birim testi eklendi (12/12 test %100 başarılı).
- **Cache Busting (`?v=4.68.0`):** Sürüm parametresi yükseltildi.

---

### 🐛 JS Sentaks Hatasının Giderilmesi (`templates/dashboard.html`)
- **Kırık JS Bloğunun Temizlenmesi:** Geçmiş entegre admin kodlarından kalan ve unclosed `try {` bloğu nedeniyle `dashboard.html` içerisindeki tüm JavaScript kodlarının çalışmasını durduran sentaks hatası **100% temizlendi**.
- **Doğrudan `onclick` Etkileşim Garantisi:** `#sendBtn` butonuna `onclick="sendDirectTextMessage()"` ve `#recordBtn` butonuna `onclick="toggleVoiceRecord()"` nitelikleri eklenerek tüm cihazlarda ve ekranlarda butonların tıklanabilirliği kesin garanti altına alındı.
- **Cache Busting (`?v=4.67.0`):** Güncellenmiş JavaScript ve CSS'lerin anında devreye girmesi için sürüm yükseltildi.

---

### 📐 Teklif & Mikrofon Buton Düzeltmesi (`templates/dashboard.html`)
- **Görsel Hizalama & Çakışma Düzeltmesi:** `#recordBtn` (Mikrofon) ve `#sendBtn` (Teklif Üret) butonları esnek bir grup konteynerine (`display: flex; gap: 8px; flex-shrink: 0;`) alınarak üst üste binme engellendi. `#sendBtn` butonuna `min-width: 120px; white-space: nowrap;` verilerek "Teklif Üret" metninin taşması ve kesilmesi %100 düzeltildi.

### 👑 Usta Özel Kilidi & Paket Yükseltme Talebi (`main.py`, `templates/dashboard.html`)
- **Paket Yükseltme Endpoint'i (`POST /api/shop/request_upgrade`):** Esnafların paket yükseltme taleplerini veritabanına kaydeden endpoint eklendi.
- **Usta Özel Kilit Etkileşimi:** Ciro kartındaki "Usta Özel" kilidine (`ciroLock`) veya yükseltme butonlarına tıklandığında cam efektli Paket Karşılaştırma Modalı (`upgradeComparisonModal`) açıldı. Esnaf `[Talebi Gönder]` butonuna bastığında talep Yönetici Onay Masasına (`/admin`) iletildi.
- **Cache Busting (`?v=4.66.0`):** Önbellek sürümü yükseltildi.

---

### 🧹 Entegre Yönetici Bölümünün Temizlenmesi (`templates/dashboard.html`)
- **`integratedAdminSection` HTML Blok Temizliği:** `dashboard.html` alt bölümünde kalan ve esnaf ekranının altında görünen `👑 SİSTEM YÖNETİCİ MASASI (ABONE & TALEP YÖNETİMİ)` entegre bölümü **tamamen silindi**.
- **Atıl Admin JS Fonksiyonlarının Silinmesi:** `dashboard.html` içerisindeki atıl kalmış `loadAdminShopsIntegrated`, `adminExtendValidityIntegrated`, `approveUpgradeIntegrated`, `rejectUpgradeIntegrated`, `toggleActiveIntegrated`, `adminChangePackageIntegrated` fonksiyonları 100% temizlendi.
- **Dükkan Paneli İzolasyonu:** Dükkan paneli (`dashboard.html`) tamamen esnaf teklif ve tamir masasına dönüştürüldü; yönetici işlemleri yalnızca bağımsız `/admin` rotasında izole edildi.
- **Cache Busting (`?v=4.65.0`):** Anında ekrana yansıma için sürüm yükseltildi.

---

### 📐 Yönetici Onay Masası %100 Tam Ekran Düzeni (`templates/admin.html`, `static/style.css`)
- **Dar Genişlik Kısıtlamasının Kaldırılması (`max-width: 900px` -> `%100`):** `.admin-workspace` ve `.app-container` alanlarındaki dar genişlik ve marjin kısıtlamaları kaldırıldı. Yönetici Onay Masası ekranın tamamını (%100 Viewport genişlik ve yüksekliği) kaplayacak şekilde boyutlandırıldı.
- **İsim & İfade Temizliği:** Kafa karışıklığı yaratan "Sistem Yönetici Paneli" ve "Sistem Yönetim Masası" ibareleri tamamen kaldırıldı. Sayfa ve sekme adı **"Yönetici Onay Masası"** (Abone ve Dükkan Yetkilendirme) olarak netleştirildi.
- **Cache Busting (`?v=4.64.0`):** Önbellek sürümü yükseltildi.

---

### 🌟 7 Günlük Pro Deneme Paketi (`cloud_storage.py`, `main.py`)
- **Varsayılan Usta Deneme Paketi (`create_shop`):** 7 Günlük Ücretsiz Denemeyi başlatan her esnafa varsayılan olarak `package: "usta"` Pro deneme paketi tanımlandı.
- **%100 Açık Dükkan Masası:** Esnaf 7 günlük deneme süresince (`daysLeft > 0`) kilit ekranına takılmadan tüm teklif motoru, PDF üretimi ve ciro kartlarını eksiksiz kullandı.

### ⛔ Deneme Dolduğunda Yöneticiye Yönlendirme Kilit Ekranı (`dashboard.html`)
- **Yöneticiye Yönlendirme Uyarısı:** 7 Günlük Deneme süresi bittiğinde (`daysLeft <= 0`) dükkan ekranı tamamen kilitlenerek esnafa *"⛔ 7 Günlük Ücretsiz Deneme Süreniz Sona Ermiştir! Dükkan hesabınızı aktifleştirmek için lütfen Yönetici ile İletişime Geçin."* uyarısı sunuldu ve direkt WhatsApp yönetici iletişim butonu eklendi.

### 🏷️ Başlık Netleştirmesi & Cache Busting (`dashboard.html`, `admin.html`)
- **Dükkan Sayfası Başlığı (`dashboard.html`):** `Dijital Ustabaşı - Dükkan Teklif & Tamir Masası` olarak netleştirildi.
- **Yönetici Sayfası Başlığı (`admin.html`):** `Dijital Ustabaşı - Sistem Yönetici Paneli` olarak korundu.
- **Cache Busting (`?v=4.63.0`):** Önbellek sürümü yükseltildi.

---

### 📐 Masaüstü Ekran Yerleşim Sabitlemesi (`static/style.css`)
- **Dış Sayfa Dikey Kaydırma Engeli (`min-width: 1024px`):** Masaüstü ekranlarda `html, body` yükseklikleri `100vh` ve `overflow: hidden` olarak sabitlendi. Dış dikey tarayıcı kaydırma çubuğu kaldırıldı.
- **İç Konteyner Esnekliği:** `.app-container`, `.workspace`, `.admin-workspace` flexbox düzeninde `flex: 1` ve `min-height: 0` yapılarak tablo ve sohbet alanlarının kendi içlerinde şık bir şekilde kayması sağlandı.
- **%100 Mobil Uyumluluk Koruması (`max-width: 1023px`):** Mobil cihazlarda doğal sayfa akışı (`overflow-y: auto`, `height: auto`) ve dokunmatik dikey kaydırma tam koruma altına alındı.

### 🛡️ Dükkan Kayıt Oturumu Hijack Engeli (`templates/index.html`, `templates/dashboard.html`)
- **Eski Admin Oturumu Temizliği:** "7 Günlük Ücretsiz Denemeyi Başlat" butonuna basıldığında veya dükkan numarası ile giriş yapıldığında yerel depolamadaki (`localStorage`) eski admin bayrakları (`is_admin_active`, `is_admin_logged_in`, `admin_key`) otomatik temizlenerek dükkan kullanıcısının yanlışlıkla admin paneline düşmesi engellendi.
- **Bağımsız Admin Rotalaması:** `dashboard.html` üzerinden gizli şifre ile yönetici girişi yapıldığında oturum doğrudan `/admin` bağımsız rotasına yönlendirildi.
- **Cache Busting (`?v=4.62.0`):** Önbellek sürümü yükseltildi.

---

### 🔒 Giriş Güvenliği & Kayıtsız Numara Engeli (`main.py`, `cloud_storage.py`, `index.html`, `dashboard.html`)
- **Otomatik Dükkan Oluşturma Engeli (`GET /api/shop`):** Kayıtsız bir telefon numarası ile `/api/shop` çağrıldığında otomatik dükkan kaydı açılması durduruldu. Veritabanında olmayan numaralar için HTTP 404 (`{"detail": "Bu telefon numarasına ait bir dükkan kaydı bulunamadı."}`) yanıtı döndürüldü.
- **7 Günlük Deneme Kayıt Endpoint'i (`POST /api/shop/register`):** Yeni dükkan oluşturma yetkisi yalnızca "7 Günlük Ücretsiz Denemeyi Başlat" formuyla sınırlanarak backend'de `/api/shop/register` endpoint'i tanımlandı.
- **Giriş Yönlendirme Koruması (`GET /`, `GET /dashboard`):** `login_phone` URL parametresi ile gelen numaranın veritabanında kaydı yoksa panele sokulması engellendi; otomatik olarak `/?error=not_registered` adresine yönlendirilerek kullanıcıya "Kayıtlı dükkan bulunamadı" bildirimi sunuldu.

### 🎨 Admin Paneli Görünüm Restorasyonu (`static/style.css`, `templates/admin.html`)
- **Görsel Stil Restorasyonu (`style.css`):** Admin panelinde bozuk/stilsiz görünen `.admin-table-container`, `.admin-table`, `th`, `td`, `.validity-btn-group`, `.btn-validity-extend` ve `.admin-workspace` sınıflarına modern cam efekti (glassmorphism), renkli yetki rozetleri ve responsive tablo tasarımı tanımlandı.
- **Cache Busting (`?v=4.61.0`):** Önbellek sürümü yükseltildi.

### 🏛️ Mimari Rota & Panel Ayrımı (`main.py`, `admin.html`, `dashboard.html`)
- **İzole Rotalar:** Admin Paneli (`/admin`), Dükkan Paneli (`/dashboard`) ve Karşılama/Kayıt Sayfası (`/`) arasındaki `admin=true` query parametre çakışmaları temizlendi. Admin ve dükkan oturumları tamamen birbirinden izole edildi.

---

### 👑 Dedicated Admin Workspace & Quote Generator Hiding
- **Yönetici Modunda Teklif Motorunun Gizlenmesi (`dashboard.html`):** Yönetici oturumunda (`admin-mode-active`), esnafa özel Sesli/Yazılı Teklif Motoru ve dükkan paneli tamamen gizlenerek (`display: none !important`) ekranda **yalnızca Yönetici Masası (Abone Tablosu)** sunuldu.
- **Cache Busting (`?v=4.60.0`):** Önbellek sürümü yükseltildi.

---

## [v3.2.0] - 2026-07-26 (Header Buton Temizliği & Abone Yönetim Tablosu)

### 🧹 Clean UI & Detailed VoltNet Subscriber Table
- **Header Fazla Buton Temizliği (`index.html`, `dashboard.html`):** Header alanındaki görünür `#btnAdminLoginHeader` ve `#btnAdminLoginDashboard` butonları tamamen kaldırıldı. Yönetici girişi yalnızca **logoya tek tıkla** modal açarak sağlanır.
- **Detaylı Abone Yönetim Tablosu Entegrasyonu (`admin.html`):** Basit kart ızgara görünümü kaldırılarak yerine **Dükkan Adı, Telefon, Paket Seçimi, Yetki Statüsü (Aktif/Askıda), Geçerlilik / Kalan Süre, Süre Uzat (+7G, +30G, +1Y)** ve **Paket Talepleri (Onayla/Reddet)** içeren VoltNet tarzı Abone Tablosu entegre edildi.
- **Cache Busting (`?v=4.59.0`):** Önbellek sürümü yükseltildi.

---

## [v3.1.0] - 2026-07-26 (JS Sentaks Parantez Düzeltmesi & %100 Çalışan Telefon Maskesi)

### 🐛 JS Scope Syntax Error Fix & Active Input Sanitization
- **Sentaks Parantez Hatası Tamiri (`index.html`, `dashboard.html`):** Script bloğunda kapatılmamış küme parantezleri (`}`) tamir edildi. Tarayıcının script derlemesini durdurması (`ReferenceError`) ve tüm JS fonksiyonlarını devre dışı bırakması kökten çözüldü.
- **Aktif Çalışan Rakam Filtresi:** `preventNonNumericInput` ve `formatTurkishPhoneInput` fonksiyonları sorunsuz derlenerek telefon alanlarında harf ve özel karakter girişi %100 engellendi.
- **Cache Busting (`?v=4.58.0`):** Önbellek sürümü yükseltildi.

---

## [v3.0.0] - 2026-07-26 (VoltNet Uyumlu Doğrudan Yönetici Girişi & %100 Kurşun Geçirmez Telefon Maskelemesi)

### 👑 VoltNet Style Direct Admin & Strict Phone Validation
- **Doğrudan Tıklanabilir Yönetici Girişi Butonu (`index.html`, `dashboard.html`):** Header alanına VoltNet mimarisiyle uyumlu, 1 tıkla modal açan turuncu cam efektli **"Yönetici Girişi"** (`#btnAdminLoginHeader`) butonu eklendi.
- **Logo Tek Tık Giriş Yeteneği (`index.html`, `dashboard.html`):** Header logosuna tıklama engelleri (3 tık / Shift zorunluluğu) kaldırılarak **TEK TIKLA (Single Click)** doğrudan `openAdminSecretModal()` çağrısı bağlandı.
- **`localStorage` Anahtar Senkronizasyonu (`index.html`, `dashboard.html`, `admin.html`):** Şifre doğrulandığında `is_admin_active`, `is_admin_logged_in` ve `admin_key` anahtarlarının tümü eşzamanlı yazılarak sayfalar arası yetkilendirme çakışmaları kökten giderildi.
- **%100 Kurşun Geçirmez Telefon Giriş Koruması (`preventNonNumericInput`):** `landingPhoneInput`, `headerPhoneInput` ve `loginPhoneInput` alanlarında harf girişini hem klavye seviyesinde (`onkeydown` prevent default) hem de girdi/yapıştırma seviyesinde (`oninput`, `onpaste`) engelleyen sıkı rakam filtresi entegre edildi.
- **Cache Busting (`?v=4.57.0`):** Önbellek sürümü yükseltildi.

---

## [v2.9.0] - 2026-07-26 (Header Logo Admin Girişi & Mükerrer Modal Temizliği)

### 👑 Stealth Admin Click Fix & Consolidated Modals
- **Mükerrer Modal & Çatışan JS Fonksiyonlarının Temizlenmesi (`dashboard.html`):** `dashboard.html` içerisindeki ikinci çakışan `#adminSecretModal` ID'li HTML bloğu kaldırıldı. Mükerrer JS fonksiyonları (`openAdminSecretModal`, `handleHeaderLogoClick`, `submitAdminSecretPassword`) konsolide edildi.
- **Tıklanabilir Logo & Efekt (`index.html`, `dashboard.html`):** Header logosuna `.logo-area` CSS `cursor: pointer`, `user-select: none` ve yumuşak hover efekti tanımlandı.
- **Kapsamlı Şifre Uyumluluğu & Doğrudan Yönetici Masası Erişimi (`/admin`):** Gizli modalda şifre onaylandığında hem `is_admin_active` hem de `admin_key` yerel depolamaya (localStorage) işlenerek entegre masa açılır; landing sayfasından `/admin` yönetim masasına otomatik yönlendirme sağlanır.
- **Cache Busting (`?v=4.56.0`):** Şablon önbellek sürümü yükseltildi.

---

## [v2.8.0] - 2026-07-26 (100% Görünmez Gizli Admin Logosu & Özel Cam Kaydırma Çubuğu)

### 🎨 Stealth Admin & Custom Scrollbar Polish (Görünmez Gizlilik & Özel Scrollbar)
- **Görünür Kilit Simgesinin ve İpuçlarının Silinmesi (`index.html`, `dashboard.html`):** Dışarıdan giren normal kullanıcıların gizli yönetici alanını kesinlikle fark etmemesi için görünür kilit simgesi ve hover tooltip yazısı tamamen kaldırıldı. Gizli giriş sadece **Shift + 3 Tık** ve **Shift + A** kombinasyonu ile çalışmaya devam eder.
- **Jilet Gibi İnce Özel Cam Kaydırma Çubuğu (`style.css`):** Tarayıcının amatör gri kaydırma çubuğu kaldırılıp yerine 6px inceliğinde turuncu-koyu cam uyumlu (`rgba(249, 115, 22, 0.4)`) ultra-modern scrollbar entegre edildi.
- **Cache Busting (`?v=4.55.0`):** Şablon önbellek sürümü yükseltildi.

---

## [v2.7.0] - 2026-07-26 (Garanti Gizli Yönetici Girişi: Inline Onclick + Shift+A Kısayolu)

### 👑 Stealth Admin Access Fix (Garanti Admin Girişi)
- **Inline `onclick="handleHeaderLogoClick(event)"` (`index.html`, `dashboard.html`):** Logoda tıklama dinleyicisinin DOM yüklenmeden önce kaçırılmaması için doğrudan satır içi `onclick` bağlandı.
- **Gizli Rozet & `Shift + A` Klavye Kısayolu:** Logoda başlık yanındaki gizli kilit rozetine basılarak veya klavyeden **Shift + A** kombinasyonu yapılarak her an Gizli Admin Şifre Modalı açılabilir.
- **Cache Busting (`?v=4.54.0`):** Şablon önbellek sürümü yükseltildi.

---

## [v2.6.0] - 2026-07-26 (Shift + Logoya 3 Tık Gizli Yönetici Giriş Mimarisi)

### 👑 Stealth Admin Access & Security (Gizli Admin Modalı)
- **Logoda `Shift + 3 Tık` Gizli Tetikleyici (`index.html`, `dashboard.html`):** Logoya Shift tuşu ile tıklayan veya 3 hızlı tık/dokunuş yapan kullanıcılara ekran karartılarak şık **Gizli Admin Şifre Modalı (`#adminSecretModal`)** açılması sağlandı.
- **Şifreli Geçiş Kontrolü (`ustabasi2026`):** Doğru şifre girildiğinde `is_admin_active=true` oturumu kaydedilerek doğrudan **Sistem Yönetici Masasına (`/?admin=true`)** yönlendirme yapıldı.
- **Cache Busting (`?v=4.53.0`):** Şablon önbellek sürümü yükseltildi.

---

## [v2.5.0] - 2026-07-26 (Jilet Gibi Tek Sütunlu Sade Mobil & Masaüstü Karşılama Ekranı)

### 🎨 Clean UX & Mobile Optimization (Tam Ekran Sadeleşme)
- **Eski Simülatör Panelinin Tamamen Temizlenmesi (`index.html`):** Görüntü kirliliği ve mobil ekran kalabalığı yaratan sol simülatör alanı tamamen kaldırıldı.
- **%100 Duyarlı Tek Sütunlu Tasarım (`max-width: 820px`):** Açılış sayfası hem masaüstünde hem mobilde jilet gibi ortalanmış tek sütunlu kurumsal kayıt ekranına dönüştürüldü.
- **Cache Busting (`?v=4.52.0`):** Şablon önbellek sürümü yükseltildi.

---

## [v2.4.0] - 2026-07-26 (05XX Canlı Telefon Maskelemesi & Buzlu Önizleme Mimarisi)

### 🔒 Security, UX & Input Masking (05XX Maskeleme & Sadeleşme)
- **Tek Tip Canlı Telefon Maskelemesi (`formatTurkishPhoneInput`):** Tüm telefon giriş kutularında harf ve özel karakter yazımı imkansız kılındı (`oninput`). Kullanıcı rakam bastıkça otomatik `05XX XXX XX XX` formatı oturtuldu.
- **Üst Header ve Orta Kayıt Kutuları Senkronizasyonu (`index.html`):** Üst header'daki "Panele Giriş Yap" kutusuna kayıtlı numara yazıldığında doğrudan panele geçilmesi, kayıtsız numara yazıldığında ise *"Dükkan bulunamadı"* uyarısıyla ortadaki deneme alanına odaklanılması sağlandı.
- **Sol Panel Buzlu Önizleme Mode (`index.html`):** Sol taraftaki sohbet simülatörü buzlu cam efekti (`backdrop-filter: blur(8px)`) ve `🔒 Örnek Sesli Teklif Önizlemesi` rozeti ile kaplandı. Mobilde tamamen gizlenerek 100% kayıt odaklı sade bir görünüm elde edildi.
- **Cache Busting (`?v=4.51.0`):** Şablon önbellek sürümü yükseltildi.

---

## [v2.3.0] - 2026-07-26 (Aktif Numara Gösterimi & Jilet Gibi Taşmasız Buton Mimarisi)

### 🐞 Fixed & Perfected (Düzeltmeler ve Mükemmelleştirmeler)
- **HATA 1 - Numarasız Panele Geçiş Engellendi (`main.py`):** Kök adreste (`/`) `login_phone` yoksa otomatik olarak `index.html` (Telefon Kayıt Ekranı) sunulması garanti altına alındı.
- **HATA 2 - Aktif Usta Numarasının Görünmesi & Çıkış Yapılabilmesi (`dashboard.html`):** `phoneInput` elementinin DOM yüklenmeden okunması hatası giderildi. Aktif usta numarası (Örn: `0532 123 45 67`) "Aktif Usta No" kutusuna net olarak yazdırıldı ve "Oturumu Kapat" butonuyla `index.html` ekranına dönülmesi sağlandı.
- **HATA 3 - Turuncu Buton Taşması Sıfırlandı (`dashboard.html`, `style.css`):** Teklif kutusu `box-sizing: border-box; overflow: hidden;` tek satır flex mimarisine kavuşturuldu. Turuncu "Teklif Üret" butonu sağ panel sınırından milimetre dışarı taşmaz.
- **Cache Busting (`?v=4.50.0`):** Şablon önbellek sürümü yükseltildi.

---

## [v2.2.0] - 2026-07-26 (Zorunlu Telefon Numaralı Giriş Akışı & Gizli Admin Mimarisi)

### 🔒 Security & Onboarding Overhaul (Güvenli Giriş & Gizli Admin)
- **Ana Sayfada Telefon Numarası Alma Zorunluluğu (`main.py`, `index.html`, `dashboard.html`):** Siteye (`/`) bağlanan kullanıcılar numara girmeden Dükkan Paneline erişemez. `index.html` üzerinde 10 haneli cep telefonu girilip doğrulandığında `dashboard.html` ekranına güvenli geçiş sağlanır.
- **Gizli Admin Giriş Yapısı:** Herkesin görebileceği açık Admin geçiş butonları kaldırıldı. Admin Paneli (`admin.html`) sadece **Shift + Logoya 3 Tık** gizli hareketiyle veya doğrudan `/?admin=true` adresi üzerinden şifreli giriş ile açılır.
- **Cache Busting (`?v=4.49.0`):** Şablon önbellek sürümü yükseltildi.

---

## [v2.1.0] - 2026-07-26 (Sistem Yönetici Masası Senkronizasyonu & Simülatör Temizliği)

### 🧹 Fixed & Synchronized (Eşitlemeler ve Düzeltmeler)
- **Admin Panel Erişimi & Şablon Senkronizasyonu (`main.py`, `admin.html`):** `/?admin=true` ve `/admin` rotalarında doğrudan `admin.html` (Sistem Yönetici Masası) şablonunun kusursuz sunulması sağlandı. `admin.html` header kısmına "🏬 Dükkan Paneline Dön" butonu eklendi.
- **Kalan Tüm Simülatör Kutu Kalıntılarının Temizlenmesi (`dashboard.html`):** Üst header'daki eski "⚙️ Simülatör (Paket Değiştirici)" kutusu tamamen silindi.
- **Cache Busting (`?v=4.48.0`):** Şablon önbellek sürümü yükseltildi.

---

## [v2.0.0] - 2026-07-26 (Kalıcı Taşmasız Duyarlı Buton Mimarisi)

### 🎨 Fixed & Improved (Düzeltmeler ve İyileştirmeler)
- **Kalıcı Taşmasız Buton Yerleşimi (`dashboard.html`, `style.css`):** Metin giriş alanı ve buton grubu (`.input-btn-group`) `flex-wrap: wrap` ve `min-width: 0` mimarisine kavuşturuldu. Dar/mobil ekranlarda "Teklif Üret" ve mikrofon butonunun ekrandan taşma veya sığmama problemi kalıcı olarak çözüldü.
- **Cache Busting Güncellemesi (`?v=4.47.0`):** Yeni buton stil kurallarının tarayıcılara anında yüklenmesi sağlandı.

---

## [v1.9.0] - 2026-07-26 (Doğrudan Ekran Üzerinde Sesli & Yazılı Teklif Motoru)

### 🚀 Added & Improved (Eklenenler ve İyileştirmeler)
- **Doğrudan Ekran Üzerinde Sesli & Yazılı Teklif Motoru (`dashboard.html`):** Dışarıya yönlendiren WhatsApp butonları tamamen kaldırıldı; yerine doğrudan sayfa üzerinde mikrofona basarak konuşmayı ve yazarak anında kurumsal PDF Teklif üretmeyi sağlayan dahili teklif motoru yerleştirildi.
- **Canlı Mikrofon & Ses Deşifre Akışı:** `MediaRecorder` ve `/api/simulate/voice` entegrasyonu ile ustanın tarayıcı üzerindeki mikrofona basıp konuştuğu ses anında PDF teklife dönüştürülüp tabloya eklenmektedir.

---

## [v1.8.0] - 2026-07-26 (Tek Birleşik Ana Adres Mimarisi - Single Root URL)

### 🚀 Changed & Streamlined (Değiştirilenler ve Sadeleştirilenler)
- **Tek Birleşik Ana Adres Mimarisi (`main.py`):** Tüm platform, usta yönetimi ve gizli Yönetici Masası tek bir birleşik ana adres olan `/` (`https://dijital-ustabasi-production.up.railway.app/`) altında toplandı.
- **Yönlendirme Protokolü (Redirect Protocol):** Eski `/dashboard` ve `/admin` adreslerinden gelen tüm istekler parametreleriyle birlikte otomatik olarak tek ana adres olan `/` ve `/?admin=true` rotasına yönlendirilir.

---

## [v1.7.0] - 2026-07-26 (Kurumsal Güven Rozetleri & Ferah Panel Revizyonu)

### 🚀 Added & Improved (Eklenenler ve İyileştirmeler)
- **Giriş Sayfası Güven & Avantaj Rozetleri (`index.html`):** Eski QR kodu kutusu kaldırılarak yerine 3 büyük avantaj rozeti (⚡ 3 Saniyede PDF, 🏷️ Plaka & Parça Tanıma, 🛡️ Bulut Depolama) ve dikkat çekici **"🚀 7 Günlük Ücretsiz Denemeyi Başlat"** CTA butonu eklendi.
- **Ferah Dükkan Paneli Ekranı (`dashboard.html`):** Dükkan panelindeki gereksiz QR kodu ve WhatsApp yönlendirmeleri tamamen silindi; ekran ustaya özel sade, ferah ve üretken bir çalışma alanına dönüştürüldü.

---

## [v1.6.0] - 2026-07-26 (Gerçek SaaS Deneme Süresi & Simülasyon Temizliği)

### 🧹 Removed & Changed (Kaldırılanlar ve Değiştirilenler)
- **Simülasyon ve Test İbarelerinin Temizlenmesi (`index.html`, `dashboard.html`):** Arayüzdeki "Simülatör", "Test Modu", "Demo Numarası" etiketleri kaldırılarak doğrudan "Dijital Ustabaşı - Akıllı Sesli Teklif & Kurumsal PDF Motoru" üretken SaaS sistemine dönüştürüldü.
- **7 Günlük Gerçek Deneme Süresi & Otomatik Kısıtlama Akışı:** Yeni dükkanların kaydolduğu andan itibaren 7 günlük ücretsiz deneme süresinin (Full Açık) başlaması, süre bittiğinde ise müşteri temsilcisine yönlendiren kilit ekranının devreye girmesi sağlandı.

---

## [v1.5.0] - 2026-07-26 (Kusursuz Mobil Uyum & WhatsApp Buton Revizyonu)

### 🎨 Improved & Fixed (İyileştirilenler ve Düzeltmeler)
- **Mobil Tam Uyumlu Ekran Düzeni (`style.css`):** iPhone ve Android ekranlarında sağa-sola kaymaları engelleyen `overflow-x: hidden` ve `@media (max-width: 768px)` kuralları eklendi. İki sütunlu alanlar mobilde tek sütuna (`grid-template-columns: 1fr`) dönüştürüldü.
- **Yüksek Kontrastlı WhatsApp Butonları (`.btn-whatsapp-cta`, `.btn-whatsapp-direct`):** WhatsApp markasının orijinal yeşili (`#25D366`), dokunma alanları en az `52px` yüksekliğe ve `15px font-size` boyutlarına çıkartıldı.
- **Cache Busting Entegrasyonu:** Tüm HTML şablonlarında statik dosya referansları `?v=4.42.0` seviyesine yükseltildi.

---

## [v1.4.0] - 2026-07-26 (Meta WhatsApp Cloud API Botu & Canlı Webhook Entegrasyonu)

### 🚀 Added (Eklenenler)
- **WhatsApp Webhook Handler Servisi (`whatsapp_bot.py`, `main.py`):** Meta WhatsApp Business Cloud API canlı entegrasyonu sağlandı.
  - **Webhook Doğrulama (`GET /api/whatsapp/webhook`):** Meta webhook `hub.verify_token` ve `hub.challenge` doğrulaması eklendi.
  - **Mesaj ve Ses Kaydı Dinleyici (`POST /api/whatsapp/webhook`):** Sanayideki ustaların attığı sesli mesajlar (voice note) ve yazılı mesajlar canlı olarak dinlenip Gemini AI / Whisper ile otomasyona bağlandı.
- **Otomatik PDF Yanıtı & Sohbet Motoru:** Üretilen ReportLab kurumsal PDF teklif bağlantısı ve detaylı fiyat özeti WhatsApp kullanıcısının sohbetine otomatik yanıt olarak gönderilir (`send_whatsapp_message`).
- **Simülatör Endpoint'i (`POST /api/whatsapp/simulate`):** Meta API anahtarları olmadan da WhatsApp bot otomasyonunun test edilebilmesi sağlandı.

---

## [v1.3.0] - 2026-07-26 (Sadece Yönetici Masası Odaklı Temiz Admin Görünümü)

### 🛡️ Changed & Improved (Değiştirilenler & İyileştirmeler)
- **Usta Kilit & Paywall Ekranının Gizlenmesi (`dashboard.html`):** Yönetici moduna geçildiğinde (`admin-mode-active`), normal dükkan sahipleri için gösterilen "Yönetim Paneli Kilitli - Çırak Paketindesiniz" paywall uyarısı (`.full-width-panel`) ve WhatsApp butonu (`.voice-cta-bar`) tamamen gizlendi (`display: none !important`).
- **Saf Yönetici Ekranı Odaklanması:** Yönetici masası açıldığında ekran tüm kalabalıktan arındırılarak sadece **Sistem Yönetici Masası (Abone & Talep Yönetimi)** masasına odaklanacak şekilde güncellendi.

---

## [v1.2.5] - 2026-07-26 (VoltNet Yüksek Yoğunluklu Abone Masası & Yükseklik Düzeltmesi)

### 🚀 Added (Eklenenler)
- **VoltNet Abone & Talep Yönetim Masası (`.admin-table`):** Kartlı görünüm yerine VoltNet tarzı yüksek yoğunluklu abone yönetim tablosu eklendi. Yönetici tüm aboneleri, yetki statülerini (Aktif/Askıda), paket seviyelerini ve süre uzatma seçeneklerini tek ekranda yönetebilir.
- **Geçerlilik Süresi Uzatma (`/api/admin/extend_validity`):** Yönetici masasına tek tıkla `+7 Gün`, `+30 Gün` ve `+1 Yıl` deneme/abonelik süresi uzatma butonları eklendi.

### 🛡️ Fixed (Düzeltmeler)
- **Yükseklik & Kaydırma (Cut-Off Düzeltmesi):** Admin modu aktif olduğunda `.app-container` ve `.workspace-dashboard` üzerindeki `90vh` yükseklik kısıtlaması otomatik kaldırıldı (`height: auto !important`). Tüm masanın kesintisiz olarak aşağıya kaydırılarak görüntülenmesi sağlandı.

---

## [v1.2.0] - 2026-07-26 (VoltNet Tarzı Birleşik & Gizli Admin Paneli)

### 🚀 Added (Eklenenler)
- **VoltNet Tarzı Gizli Admin Tetikleyicisi (`dashboard.html`):** Header Logoya 3 kez tıklama (veya Shift + Tık) ile çalışan gizli yönetici şifre modalı (`#adminSecretModal`) eklendi.
- **Birleşik Yönetici Masası (`#integratedAdminSection`):** Ayrı kamuya açık `/admin` sayfası yerine, doğrudan `dashboard.html` içerisine entegre edilmiş şifreli Yönetici Masası eklendi. Şifre doğrulanmadıkça yetkisiz kullanıcılar ve ziyaretçiler yönetici alanlarını göremez.
- **Otomatik Rota Yönlendirmesi (`main.py`):** `/admin` URL'i doğrudan `/dashboard?admin=true` birleşik moduna yönlendirildi.

---

## [v1.1.0] - 2026-07-26 (Güvenlik & Canlıya Alma Güncellemesi)

### 🚀 Added (Eklenenler)
- **Railway Deployment Desteği:** `Procfile` eklenerek dynamic `${PORT:-8080}` port bağlama desteği sağlandı.
- **Admin Güvenlik Kalkanı (`verify_admin_key`):** `/api/admin/shops`, `/api/admin/approve_upgrade`, `/api/admin/reject_upgrade` ve `/api/admin/toggle_active` uç noktalarına `X-Admin-Key` başlık kontrolü eklendi. Yetkisiz istekler 401 durum kodu ile engellendi.
- **Dokümantasyon:** Proje köküne `README.md` ve `.env.example` şablonu eklendi.
- **API Entegrasyon Testleri:** `test_dijital_ustabasi.py` içerisine FastAPI `TestClient` ile admin yetkilendirme ve PDF indirme güvenlik kontrollerini sınayan yeni testler eklendi.

### 🛡️ Changed (Değiştirilenler & Düzeltmeler)
- **Cache Busting Entegrasyonu:** `index.html`, `dashboard.html` ve `admin.html` içerisindeki `/static/style.css` bağlantılarına `?v=4.19.0` sürüm parametresi eklendi.
- **Admin Arayüzü Güvenliği:** `admin.html` arayüzü `X-Admin-Key` gönderecek şekilde JS uç noktaları yenilendi.

---

## [v1.0.0] - 2026-07-20 (İlk Sürüm)
- Sesli ve yazılı WhatsApp mesajlarının Gemini/Whisper ile ayrıştırılması.
- ReportLab ile kurumsal Türkçe PDF teklif oluşturucu.
- Çırak, Kalfa, Usta paket sistemi ve Dashboard simülatör ekranları.
