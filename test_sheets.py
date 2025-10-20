#!/usr/bin/env python3
"""
Test Google Sheets connection
"""

import os

print("🔍 Checking Google Sheets setup...\n")

# Check 1: Credentials file
if os.path.exists('google_credentials.json'):
    print("✅ google_credentials.json found")
    
    # Check file size
    size = os.path.getsize('google_credentials.json')
    print(f"   File size: {size} bytes")
    
    if size < 100:
        print("   ⚠️ File seems too small - might be corrupted")
else:
    print("❌ google_credentials.json NOT FOUND")
    print("\n📋 To fix this:")
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Create/select project")
    print("3. Enable Google Sheets API")
    print("4. Create Service Account:")
    print("   - Credentials → Create Credentials → Service Account")
    print("   - Download JSON key")
    print("5. Rename downloaded file to 'google_credentials.json'")
    print("6. Place it in the MiraiAi folder")
    print("\nThen run this test again!")
    exit(1)

# Check 2: Packages
print("\n📦 Checking packages...")
try:
    import gspread
    print("✅ gspread installed")
except ImportError:
    print("❌ gspread not installed")
    print("   Run: pip install gspread")
    exit(1)

try:
    from oauth2client.service_account import ServiceAccountCredentials
    print("✅ oauth2client installed")
except ImportError:
    print("❌ oauth2client not installed")
    print("   Run: pip install oauth2client")
    exit(1)

# Check 3: Connection
print("\n🔗 Testing connection...")
try:
    from google_sheets_storage import GoogleSheetsStorage
    
    storage = GoogleSheetsStorage()
    
    if storage.enabled:
        print("✅ Connected to Google Sheets!")
        print(f"   Sheet ID: 1hardTfwdlSpk55wpDoXIL1HwEQdJXh6N4QcXl9rgNzM")
        print(f"   Current rows: {storage.sheet.row_count}")
        
        # Check 4: Test write
        print("\n✍️ Testing write...")
        result = storage.save_conversation("TestUser", "Test question", "Test answer")
        
        if result:
            print("✅ Test write successful!")
            print(f"   New row count: {storage.sheet.row_count}")
            print("\n🎉 Everything is working!")
            print("   Check your sheet: https://docs.google.com/spreadsheets/d/1hardTfwdlSpk55wpDoXIL1HwEQdJXh6N4QcXl9rgNzM/edit")
        else:
            print("❌ Test write failed")
            print("   Check if sheet is shared with service account")
    else:
        print("❌ Could not connect to Google Sheets")
        print("   Check the error messages above")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    print("\nFull error:")
    traceback.print_exc()
    
    print("\n💡 Common issues:")
    print("1. Sheet not shared with service account email")
    print("2. Wrong sheet ID in google_sheets_storage.py")
    print("3. Credentials file is invalid/corrupted")
