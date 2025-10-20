# Deploy with Google Sheets Storage

## 🚀 How to Deploy with Credentials

Your `google_credentials.json` is **NOT** in GitHub (for security), but your deployed bot needs it. Here's how to add it:

---

## Option 1: Render.com (Recommended)

### Step 1: Convert JSON to Base64
```bash
cd /home/kiyotoka/Desktop/MiraiAi
base64 google_credentials.json > credentials_base64.txt
cat credentials_base64.txt
```

Copy the output (long string of characters).

### Step 2: Add Environment Variable on Render

1. Go to your Render dashboard: https://dashboard.render.com/
2. Select your **MiraiAi** web service
3. Go to **"Environment"** tab
4. Click **"Add Environment Variable"**
5. Add:
   - **Key**: `GOOGLE_CREDENTIALS_BASE64`
   - **Value**: Paste the base64 string you copied
6. Click **"Save Changes"**
7. Render will automatically redeploy

### Step 3: Update Code to Use Environment Variable

The code will automatically decode and use it!

---

## Option 2: Heroku

### Step 1: Convert JSON to Base64
```bash
base64 google_credentials.json > credentials_base64.txt
cat credentials_base64.txt
```

### Step 2: Add Config Var
```bash
heroku config:set GOOGLE_CREDENTIALS_BASE64="paste_your_base64_here" -a your-app-name
```

Or via dashboard:
1. Go to Heroku dashboard
2. Select your app
3. Settings → Config Vars → Reveal Config Vars
4. Add:
   - **KEY**: `GOOGLE_CREDENTIALS_BASE64`
   - **VALUE**: Your base64 string

---

## Option 3: Railway

1. Go to Railway dashboard
2. Select your project
3. Variables tab
4. Add new variable:
   - **Name**: `GOOGLE_CREDENTIALS_BASE64`
   - **Value**: Your base64 string
5. Redeploy

---

## 🔧 Update the Code

Now update `google_sheets_storage.py` to handle both local and deployed scenarios:

```python
import os
import base64
import json
import tempfile

def get_credentials_file():
    """Get credentials file path (works locally and on deployment)"""
    
    # Check if local file exists (for local development)
    if os.path.exists('google_credentials.json'):
        return 'google_credentials.json'
    
    # Check if environment variable exists (for deployment)
    base64_creds = os.getenv('GOOGLE_CREDENTIALS_BASE64')
    if base64_creds:
        # Decode base64 and create temporary file
        creds_json = base64.b64decode(base64_creds).decode('utf-8')
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        temp_file.write(creds_json)
        temp_file.close()
        
        return temp_file.name
    
    return None
```

---

## 📝 Quick Setup Script

I'll create an updated version that handles both local and deployment automatically.

---

## ✅ Verification

After deployment:

1. Check deployment logs for:
   ```
   ✅ Google Sheets storage initialized
   ```

2. Send a test message to your bot

3. Check your Google Sheet for new rows

---

## 🔒 Security Notes

✅ **Good Practices:**
- Credentials stored as environment variables (encrypted by platform)
- Not in GitHub repository
- Not in plain text in code

❌ **Never Do:**
- Commit `google_credentials.json` to GitHub
- Share credentials in public
- Hardcode credentials in code

---

## 🆘 Troubleshooting

### "Credentials not found" on deployment
- Make sure you added `GOOGLE_CREDENTIALS_BASE64` environment variable
- Check the base64 string is complete (no line breaks)
- Redeploy after adding environment variable

### "Invalid credentials" error
- Regenerate the base64: `base64 google_credentials.json`
- Make sure you copied the entire output
- No extra spaces or line breaks

### Sheet not updating
- Check deployment logs for errors
- Verify sheet is shared with service account email
- Test locally first with `python3 test_sheets.py`

---

## 📊 How It Works

**Local Development:**
```
Bot → Reads google_credentials.json → Connects to Sheet
```

**Deployment:**
```
Bot → Reads GOOGLE_CREDENTIALS_BASE64 env var → Decodes → Creates temp file → Connects to Sheet
```

Both work seamlessly! 🎉
