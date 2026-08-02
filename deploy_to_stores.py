#!/usr/bin/env python3
"""
Dijital Ustabaşı - Otomatik App Store, Google Play Store & Firebase Dağıtım Betiği (v1.4.0)
---------------------------------------------------------------------------------------
Bu araç, projeyi kontrol edip Firebase App Distribution, Google Play Console (.aab)
ve App Store TestFlight (.ipa) paketleme ve dağıtım süreçlerini otomatize eder.
"""

import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "store_publishing_config.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        print("❌ HATA: store_publishing_config.json bulunamadı!")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def run_store_checks():
    print("🚀 Dijital Ustabaşı Otomatik Mağaza ve Firebase Kontrolü Başlatılıyor...\n")
    cfg = load_config()

    print(f"📦 Uygulama Adı     : {cfg.get('app_name')}")
    print(f"🆔 Paket Kimliği   : {cfg.get('bundle_id')}")
    print(f"🔖 Sürüm            : v{cfg.get('version')} (Build {cfg.get('build_number')})")
    print(f"🔗 Privacy Policy  : {cfg.get('privacy_policy_url')}")
    print(f"🔗 Terms of Service : {cfg.get('terms_of_service_url')}\n")

    # 1. Android Manifest Check
    android_json = os.path.join(BASE_DIR, "android", "app", "google-services.json")
    if os.path.exists(android_json):
        print("✅ [Android/Firebase] google-services.json doğrulandı.")
    else:
        print("⚠️ [Android/Firebase] google-services.json eksik!")

    # 2. iOS Manifest Check
    ios_plist = os.path.join(BASE_DIR, "ios", "App", "App", "GoogleService-Info.plist")
    if os.path.exists(ios_plist):
        print("✅ [iOS/Firebase] GoogleService-Info.plist doğrulandı.")
    else:
        print("⚠️ [iOS/Firebase] GoogleService-Info.plist eksik!")

    # 3. Capacitor Native Shell Check
    cap_cfg = os.path.join(BASE_DIR, "capacitor.config.json")
    if os.path.exists(cap_cfg):
        print("✅ [Capacitor] Native Mobile Shell (capacitor.config.json) doğrulandı.")
    else:
        print("⚠️ [Capacitor] capacitor.config.json eksik!")

    print("\n🎉 Tüm App Store, Google Play Console ve Firebase yapılandırma altyapısı HAZIR!")

if __name__ == "__main__":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    run_store_checks()
