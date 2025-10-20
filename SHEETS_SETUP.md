# Google Sheets Setup - Quick Guide

## 📊 Your Sheet
https://docs.google.com/spreadsheets/d/1hardTfwdlSpk55wpDoXIL1HwEQdJXh6N4QcXl9rgNzM/edit

## 🚀 Quick Setup (3 steps)

### Step 1: Install Packages
```bash
pip install gspread oauth2client
```

### Step 2: Create Service Account

1. Go to: https://console.cloud.google.com/
2. Create new project (or select existing)
3. Enable **Google Sheets API**:
   - APIs & Services → Library → Search "Google Sheets API" → Enable
4. Create **Service Account**:
   - APIs & Services → Credentials → Create Credentials → Service Account
   - Name: `miraibot`
   - Click "Create and Continue" → Done
5. **Download JSON Key**:
   - Click on the service account you created
   - Keys tab → Add Key → Create new key → JSON
   - Save as `google_credentials.json` in MiraiAi folder

### Step 3: Share Your Sheet

1. Open the JSON file you downloaded
2. Find the email (looks like: `miraibot@xxxxx.iam.gserviceaccount.com`)
3. Copy that email
4. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1hardTfwdlSpk55wpDoXIL1HwEQdJXh6N4QcXl9rgNzM/edit
5. Click **Share** button
6. Paste the service account email
7. Give **Editor** permission
8. Click **Send**

## ✅ Test It

```bash
python3 -c "
from google_sheets_storage import GoogleSheetsStorage
storage = GoogleSheetsStorage()
if storage.enabled:
    print('✅ Connected!')
    storage.save_conversation('TestUser', 'Hello', 'Hi there!')
    print('✅ Test data saved!')
else:
    print('❌ Not connected')
"
```

## 🤖 Run Bot

```bash
python3 telegram_bot.py
```

Now every conversation will be saved to your sheet with:
- **Username** (column A)
- **User Question** (column B)  
- **Bot Answer** (column C)

## 🔍 Troubleshooting

**Error: "Spreadsheet not found"**
- Make sure you shared the sheet with service account email
- Check the email has "Editor" permission

**Error: "Credentials not found"**
- Make sure `google_credentials.json` is in MiraiAi folder
- File name must be exactly `google_credentials.json`

**Bot runs but doesn't save**
- Check bot logs for: `✅ Connected to Google Sheet`
- If you see `⚠️ google_credentials.json not found`, credentials are missing

## 📝 View Data

Open your sheet: https://docs.google.com/spreadsheets/d/1hardTfwdlSpk55wpDoXIL1HwEQdJXh6N4QcXl9rgNzM/edit

You'll see:
```
Username       | User Question        | Bot Answer
---------------|---------------------|------------------
Kiyotoka       | Hi                  | Hello! How are you?
Kiyotoka       | I'm feeling sad     | I hear you...
```

That's it! 🎉
