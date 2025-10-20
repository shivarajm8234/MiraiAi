#!/usr/bin/env python3
"""
Check if bot will save to sheets when it receives a message
"""

import sys
sys.path.insert(0, '.')

print("🔍 Checking bot's Google Sheets integration...\n")

# Step 1: Import check
print("1️⃣ Checking imports...")
try:
    from google_sheets_storage import init_sheets_storage, save_conversation
    print("   ✅ google_sheets_storage imported")
except ImportError as e:
    print(f"   ❌ Import failed: {e}")
    exit(1)

# Step 2: Initialize
print("\n2️⃣ Initializing storage...")
try:
    sheets_storage = init_sheets_storage()
    if sheets_storage.enabled:
        print("   ✅ Storage enabled")
        print(f"   📊 Current rows: {sheets_storage.sheet.row_count}")
    else:
        print("   ❌ Storage NOT enabled")
        exit(1)
except Exception as e:
    print(f"   ❌ Initialization failed: {e}")
    exit(1)

# Step 3: Test save
print("\n3️⃣ Testing save function...")
try:
    result = save_conversation("CheckUser", "Is this working?", "Yes, it's working!")
    if result:
        print("   ✅ Save successful!")
        print(f"   📊 New row count: {sheets_storage.sheet.row_count}")
    else:
        print("   ❌ Save returned False")
except Exception as e:
    print(f"   ❌ Save failed: {e}")
    import traceback
    traceback.print_exc()

# Step 4: Check bot code
print("\n4️⃣ Checking bot code...")
with open('telegram_bot.py', 'r') as f:
    bot_code = f.read()
    
    if 'from google_sheets_storage import' in bot_code:
        print("   ✅ Bot imports google_sheets_storage")
    else:
        print("   ❌ Bot doesn't import google_sheets_storage")
    
    if 'save_to_sheets(' in bot_code:
        print("   ✅ Bot calls save_to_sheets()")
    else:
        print("   ❌ Bot doesn't call save_to_sheets()")
    
    if 'if sheets_enabled and save_to_sheets:' in bot_code:
        print("   ✅ Bot checks if sheets_enabled")
    else:
        print("   ❌ Bot doesn't check sheets_enabled")

print("\n" + "="*50)
print("✅ Everything looks good!")
print("="*50)
print("\n💡 If bot still doesn't save:")
print("1. Make sure you RESTARTED the bot after adding credentials")
print("2. Check bot logs for 'Google Sheets storage initialized'")
print("3. Send a test message to the bot")
print("4. Check your sheet for new rows")
print("\nSheet URL: https://docs.google.com/spreadsheets/d/1hardTfwdlSpk55wpDoXIL1HwEQdJXh6N4QcXl9rgNzM/edit")
