import os
import unittest
import tempfile
from datetime import datetime, timedelta
try:
    from projects.dijital_ustabasi.parser import turkish_word_to_number, rule_based_parser, normalize_turkish_plate_text
    from projects.dijital_ustabasi.pdf_generator import generate_quote_pdf, register_turkish_fonts
    from projects.dijital_ustabasi.cloud_storage import CloudStorage
except ModuleNotFoundError:
    from parser import turkish_word_to_number, rule_based_parser, normalize_turkish_plate_text
    from pdf_generator import generate_quote_pdf, register_turkish_fonts
    from cloud_storage import CloudStorage


class TestDijitalUstabasi(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.storage = CloudStorage(storage_dir=self.test_dir.name)

    def tearDown(self):
        if hasattr(self, "storage") and hasattr(self.storage, "engine"):
            try:
                self.storage.engine.dispose()
            except Exception:
                pass
        try:
            self.test_dir.cleanup()
        except Exception:
            pass

    def test_turkish_word_to_number(self):
        self.assertEqual(turkish_word_to_number("bin"), 1000)
        self.assertEqual(turkish_word_to_number("beş yüz"), 500)
        self.assertEqual(turkish_word_to_number("bin beş yüz"), 1500)
        self.assertEqual(turkish_word_to_number("iki buçuk"), 2500)
        self.assertEqual(turkish_word_to_number("yedi buçuk"), 7500)
        self.assertEqual(turkish_word_to_number("on iki bin"), 12000)
        self.assertEqual(turkish_word_to_number("kırk beş bin"), 45000)

    def test_normalize_turkish_plate_text(self):
        res1 = rule_based_parser("otuz dört a b c 123 Egea yağ değişimi 1500 TL")
        self.assertEqual(res1.get("plaka"), "34ABC123")
        res2 = rule_based_parser("34 ali veli 555 Clio triger seti 2500 TL")
        self.assertEqual(res2.get("plaka"), "34AV555")

    def test_rule_based_parser_simple(self):
        text = "34 ABC 123 Fiat Egea disk değişimi 2500 lira ve balata değişimi 1200 TL usta notu diskler orijinal"
        res = rule_based_parser(text)
        
        self.assertEqual(res["plaka"], "34ABC123")
        self.assertEqual(res["vehicle"], "Fiat Egea")
        self.assertEqual(res["usta_note"], "Diskler orijinal")
        
        self.assertEqual(len(res["items"]), 2)
        self.assertEqual(res["items"][0]["description"], "Disk değişimi")
        self.assertEqual(res["items"][0]["price"], 2500.0)
        self.assertEqual(res["items"][1]["description"], "Balata değişimi")
        self.assertEqual(res["items"][1]["price"], 1200.0)

    def test_rule_based_parser_text_numbers(self):
        text = "06 XYZ 987 Volkswagen Golf periyodik bakım bin beş yüz lira, ön balatalar iki buçuk"
        res = rule_based_parser(text)
        
        self.assertEqual(res["plaka"], "06XYZ987")
        self.assertEqual(res["vehicle"], "Volkswagen Golf")
        self.assertEqual(len(res["items"]), 2)
        self.assertEqual(res["items"][0]["description"], "Periyodik bakım")
        self.assertEqual(res["items"][0]["price"], 1500.0)
        self.assertEqual(res["items"][1]["description"], "Ön balatalar")
        self.assertEqual(res["items"][1]["price"], 2500.0)

    def test_pdf_generation(self):
        pdf_path = os.path.join(self.test_dir.name, "test_teklif.pdf")
        items = [
            {"description": "Periyodik Bakım", "price": 1500.0},
            {"description": "Ön Balata Değişimi", "price": 1000.0}
        ]
        
        subtotal, vat, total, cash_total = generate_quote_pdf(
            shop_name="Test Oto Servis",
            phone_number="+905555555555",
            plaka="34ABC123",
            vehicle="Fiat Egea",
            items=items,
            output_path=pdf_path,
            validity_days=7,
            custom_note="Test Usta Notu"
        )
        
        self.assertTrue(os.path.exists(pdf_path))
        self.assertTrue(os.path.getsize(pdf_path) > 0)
        
        self.assertEqual(subtotal, 2500.0)
        self.assertEqual(vat, 500.0)
        self.assertEqual(total, 3000.0)
        self.assertEqual(cash_total, 2700.0)

    def test_database_operations(self):
        shop = self.storage.get_or_create_shop("+905321234567")
        self.assertEqual(shop["phone_number"], "5321234567")
        self.assertEqual(shop["name"], "Oto Servis")
        self.assertEqual(shop["package"], "usta")
        
        updated_shop = self.storage.update_shop_package("+905321234567", "usta")
        self.assertEqual(updated_shop["phone_number"], "5321234567")
        self.assertEqual(updated_shop["package"], "usta")
        
        shop_refetched = self.storage.get_shop("+905321234567")
        self.assertEqual(shop_refetched["package"], "usta")
        self.assertTrue(shop_refetched.get("is_active", True))
        
        self.storage.update_shop_active_status("+905321234567", False)
        shop_refetched2 = self.storage.get_shop("+905321234567")
        self.assertFalse(shop_refetched2.get("is_active", True))
        
        self.storage.update_shop_active_status("+905321234567", True)
        
        self.storage.save_quote(
            phone_number="+905321234567",
            plaka="34XYZ789",
            vehicle="Audi A4",
            items=[{"description": "Disk Aynası", "price": 3200.0}],
            subtotal=3200.0,
            vat=640.0,
            total_price=3840.0,
            discount_price=3456.0,
            pdf_filename="teklif_test.pdf"
        )
        
        quotes = self.storage.get_quotes("+905321234567")
        self.assertEqual(len(quotes), 1)
        self.assertEqual(quotes[0]["plaka"], "34XYZ789")
        self.assertEqual(quotes[0]["vehicle"], "Audi A4")
        self.assertEqual(quotes[0]["status"], "beklemede")

    def test_shop_identity_update(self):
        self.storage.get_or_create_shop("+905559998877")
        updated = self.storage.update_shop_identity("+905559998877", "Yeni Hizmet Oto", "http://my.logo/url.png", "2026-07-10T12:00:00Z")
        self.assertIsNotNone(updated)
        self.assertEqual(updated["phone_number"], "5559998877")
        self.assertEqual(updated["name"], "Yeni Hizmet Oto")
        self.assertEqual(updated["logo_url"], "http://my.logo/url.png")
        self.assertEqual(updated["created_at"], "2026-07-10T12:00:00Z")

    def test_quote_status_update(self):
        q = self.storage.save_quote(
            phone_number="+905559998877",
            plaka="34AAA111",
            vehicle="Renault Clio",
            items=[{"description": "Yağ Filtresi", "price": 400.0}],
            subtotal=400.0,
            vat=80.0,
            total_price=480.0,
            discount_price=430.0,
            pdf_filename="clio_teklif.pdf"
        )
        
        self.assertEqual(q["status"], "beklemede")
        updated_q = self.storage.update_quote_status(q["quote_id"], "onaylandi")
        self.assertIsNotNone(updated_q)
        self.assertEqual(updated_q["status"], "onaylandi")

    def test_password_authentication(self):
        # Create shop with password
        shop = self.storage.create_shop("+905329990011", password="secret123password", name="Lider Oto")
        self.assertIsNotNone(shop)
        
        # Verify valid login
        success, msg, verified_shop = self.storage.verify_shop_login("+905329990011", "secret123password")
        self.assertTrue(success)
        self.assertEqual(verified_shop["phone_number"], "5329990011")
        
        # Verify invalid login
        success_invalid, msg_invalid, _ = self.storage.verify_shop_login("+905329990011", "wrongpassword")
        self.assertFalse(success_invalid)
        self.assertIn("Hatalı şifre", msg_invalid)
        
        # Test password update
        self.storage.update_shop_password("+905329990011", "newsecret456")
        success_new, _, _ = self.storage.verify_shop_login("+905329990011", "newsecret456")
        self.assertTrue(success_new)


class TestFastAPIIntegration(unittest.TestCase):
    def setUp(self):
        try:
            from projects.dijital_ustabasi.main import app, storage
        except ModuleNotFoundError:
            from main import app, storage
        from fastapi.testclient import TestClient
        self.client = TestClient(app)
        self.storage = storage

    def test_admin_auth_security(self):
        res = self.client.get("/api/admin/shops")
        self.assertEqual(res.status_code, 401)
        
        res_invalid = self.client.get("/api/admin/shops", headers={"X-Admin-Key": "wrongpassword"})
        self.assertEqual(res_invalid.status_code, 401)

        res_valid = self.client.get("/api/admin/shops", headers={"X-Admin-Key": "ustabasi2026"})
        self.assertEqual(res_valid.status_code, 200)

    def test_simulate_text_endpoint(self):
        phone_raw = "5551112233"
        self.storage.delete_shop(phone_raw)
        self.storage.create_shop(phone_raw, name="Fresh Simulate Shop")
        
        payload = {
            "phone_number": phone_raw,
            "text": "34 ABC 999 Renault Clio yağ değişimi 1500 TL"
        }
        res = self.client.post("/api/simulate/text", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data.get("success"))
        self.assertIn("download_url", data)

    def test_unified_single_page_app_route(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Dijital Ustabaşı", res.text)

    def test_package_archive_limits_policy(self):
        phone_raw = "05554443322"
        # Ensure clean state for test shop
        self.storage.delete_shop("5554443322")

        self.client.post("/api/shop/register", json={"phone_number": phone_raw, "password": "testpassword123", "shop_name": "Test Package Limits Shop"})
        self.storage.update_shop_identity("5554443322", "Test Package Limits Shop", "", created_at=datetime.now().isoformat())
        
        # Create a quote
        self.client.post("/api/simulate/text", json={"phone_number": phone_raw, "text": "34 LIMIT 01 Fiat Egea bakim 2000 TL"})
        
        # 1. Active trial shop gets unlimited archive (visible quotes > 0)
        res_trial = self.client.get("/api/quotes?phone_number=5554443322")
        self.assertEqual(res_trial.status_code, 200)
        data_trial = res_trial.json()
        self.assertTrue(data_trial.get("is_in_trial"))
        self.assertGreaterEqual(len(data_trial.get("quotes", [])), 1)

        # 2. Kalfa package shop gets up to 15 quotes archive (when trial expires)
        past_created = (datetime.now() - timedelta(days=8)).isoformat()
        future_expires = (datetime.now() + timedelta(days=30)).isoformat()
        self.storage.update_shop_identity("5554443322", "Test Package Limits Shop", "", created_at=past_created)
        self.storage.update_shop_expiration("5554443322", future_expires)
        self.storage.update_shop_package("5554443322", "kalfa")

        res_kalfa = self.client.get("/api/quotes?phone_number=5554443322")
        self.assertEqual(res_kalfa.status_code, 200)
        data_kalfa = res_kalfa.json()
        self.assertEqual(data_kalfa.get("package"), "kalfa")
        self.assertLessEqual(len(data_kalfa.get("quotes", [])), 15)

    def test_super_admin_authentication(self):
        res = self.client.post("/api/shop/login", json={"phone_number": "5555105635", "password": "DijitalAdmin2026!"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data.get("success"))
        shop = data.get("shop", {})
        self.assertTrue(shop.get("is_admin"))
        self.assertEqual(shop.get("package"), "usta")

    def test_html_templates_js_syntax_validation(self):
        import re
        templates_dir = os.path.join(os.path.dirname(__file__), "templates")
        if not os.path.exists(templates_dir):
            return
            
        for filename in os.listdir(templates_dir):
            if filename.endswith(".html"):
                filepath = os.path.join(templates_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                scripts = re.findall(r'<script.*?>(.*?)</script>', content, re.DOTALL)
                for i, script in enumerate(scripts):
                    stack = []
                    for char in script:
                        if char == '{':
                            stack.append('{')
                        elif char == '}':
                            self.assertTrue(len(stack) > 0, f"Unmatched closing brace '}}' in {filename} script #{i+1}")
                            stack.pop()
                    self.assertEqual(len(stack), 0, f"Unclosed opening brace '{{' ({len(stack)} remaining) in {filename} script #{i+1}")

    def test_whatsapp_webhook_and_simulate(self):
        # 1. Verification GET request
        res_verify = self.client.get("/api/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=ustabasi_verify_secret_2026&hub.challenge=CHALLENGE123")
        self.assertEqual(res_verify.status_code, 200)
        self.assertEqual(res_verify.text, "CHALLENGE123")

        # 2. Invalid Verification Token
        res_fail = self.client.get("/api/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=wrong_token&hub.challenge=CHALLENGE123")
        self.assertEqual(res_fail.status_code, 403)

        # 3. Simulate WhatsApp Quote Request
        res_sim = self.client.post("/api/whatsapp/simulate", json={"phone_number": "5559876543", "message": "34 WAPP 99 Fiat Egea balata degisimi 1800 TL"})
        self.assertEqual(res_sim.status_code, 200)
        data_sim = res_sim.json()
        self.assertTrue(data_sim.get("success"))
        self.assertIn("whatsapp_message", data_sim)

    def test_iso_date_expiration_check_with_trailing_z(self):
        # Create a shop with an expired date string containing trailing 'Z'
        past_expired_iso = (datetime.now() - timedelta(days=2)).isoformat() + "Z"
        self.storage.create_shop("+905553332211", name="Expired Test Shop")
        self.storage.update_shop_expiration("+905553332211", past_expired_iso)
        
        # Verify that check_shop_access correctly parses trailing Z and enforces 403 Forbidden
        res = self.client.get("/api/quotes?phone_number=5553332211")
        self.assertEqual(res.status_code, 403)
        self.assertIn("Paket / deneme süreniz sona ermiştir", res.json().get("detail", ""))

    def test_devops_health_check_endpoint(self):
        res = self.client.get("/healthz")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("status"), "healthy")
        self.assertEqual(data.get("app_name"), "Dijital Ustabaşı")
        self.assertIn("version", data)

if __name__ == '__main__':
    unittest.main()
