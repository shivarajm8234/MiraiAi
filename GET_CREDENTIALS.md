# Get Google Sheets Credentials - Step by Step

## 🎯 Goal
Get the `google_credentials.json` file to enable conversation storage.

---

## 📝 Step-by-Step Instructions

### Step 1: Go to Google Cloud Console
Open: https://console.cloud.google.com/

### Step 2: Create or Select Project
- Click **"Select a project"** (top left)
- Click **"New Project"**
- Name: `MiraiBot` (or any name)
- Click **"Create"**
- Wait for project to be created
- Make sure it's selected (check top left)

### Step 3: Enable Google Sheets API
1. In the search bar (top), type: **"Google Sheets API"**
2. Click on **"Google Sheets API"**
3. Click **"Enable"** button
4. Wait for it to enable (~10 seconds)

### Step 4: Create Service Account
1. Click **"Credentials"** (left sidebar)
2. Click **"+ Create Credentials"** (top)
3. Select **"Service Account"**
4. Fill in:
   - **Service account name**: `miraibot-sheets`
   - **Service account ID**: (auto-filled)
5. Click **"Create and Continue"**
6. Skip optional steps, click **"Done"**

### Step 5: Download JSON Key
1. You'll see your service account in the list
2. Click on the **service account email** (looks like: `miraibot-sheets@xxxxx.iam.gserviceaccount.com`)
3. Go to **"Keys"** tab
4. Click **"Add Key"** → **"Create new key"**
5. Choose **"JSON"** format
6. Click **"Create"**
7. File will download automatically (e.g., `miraibot-xxxxx.json`)

### Step 6: Rename and Move File
1. Find the downloaded file (usually in Downloads folder)
2. **Rename it to**: `google_credentials.json` (exactly this name!)
3. **Move it to**: `/home/kiyotoka/Desktop/MiraiAi/` folder

### Step 7: Get Service Account Email
1. Open the `google_credentials.json` file with a text editor
2. Find the line with `"client_email"`
3. Copy the email (looks like: `miraibot-sheets@xxxxx.iam.gserviceaccount.com`)

### Step 8: Share Google Sheet
1. Open your sheet: https://docs.google.com/spreadsheets/d/1hardTfwdlSpk55wpDoXIL1HwEQdJXh6N4QcXl9rgNzM/edit
2. Click **"Share"** button (top right)
3. **Paste the service account email** you copied
4. Set permission to **"Editor"**
5. **Uncheck** "Notify people" (it's a bot, not a person)
6. Click **"Share"** or **"Send"**

### Step 9: Test Connection
```bash
cd /home/kiyotoka/Desktop/MiraiAi
python3 test_sheets.py
```

You should see:
```
✅ google_credentials.json found
✅ gspread installed
✅ oauth2client installed
✅ Connected to Google Sheets!
✅ Test write successful!
🎉 Everything is working!
```

### Step 10: Run Bot
```bash
python3 telegram_bot.py
```

Now every conversation will be saved! 🎉

---

## 🔍 Troubleshooting

### Error: "google_credentials.json not found"
- Make sure file is in `/home/kiyotoka/Desktop/MiraiAi/` folder
- File name must be exactly `google_credentials.json` (no spaces, no .txt)

### Error: "Spreadsheet not found"
- Make sure you shared the sheet with service account email
- Check the email in google_credentials.json matches what you shared

### Error: "Permission denied"
- Service account needs "Editor" permission, not just "Viewer"
- Re-share the sheet with correct permission

### Error: "Invalid credentials"
- Download a new JSON key from Google Cloud Console
- Make sure you selected JSON format (not P12)

---

## 📊 Verify It's Working

1. Send a message to your bot on Telegram
2. Check your Google Sheet: https://docs.google.com/spreadsheets/d/1hardTfwdlSpk55wpDoXIL1HwEQdJXh6N4QcXl9rgNzM/edit
3. You should see a new row with:
   - Username
   - User Question  
   - Bot Answer

---

## 🎥 Visual Guide

If you need visual help, search YouTube for:
- "How to create Google Cloud service account"
- "Google Sheets API Python tutorial"

---

**Time needed**: ~5 minutes  
**Cost**: Free (Google Cloud free tier)
