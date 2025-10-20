# Bot Troubleshooting Guide

## 🔴 Error: "Conflict: terminated by other getUpdates request"

This means **multiple bot instances are running simultaneously**. Telegram only allows one active connection per bot.

### Quick Fix

**Option 1: Use the stop script**
```bash
./stop_bot.sh
```

**Option 2: Manual kill**
```bash
# Find the process
ps aux | grep telegram_bot.py

# Kill by process ID
kill <PID>

# Or kill all instances
pkill -f telegram_bot.py
```

**Option 3: Force kill**
```bash
pkill -9 -f telegram_bot.py
```

### Common Causes

1. **Multiple terminals** - You started the bot in different terminal windows
2. **Background process** - Bot is running in the background with `&`
3. **Deployed instance** - Bot is running on a server (Render, Heroku, etc.)
4. **Jupyter notebook** - Bot cell is still running in a notebook

### Check Running Instances

```bash
# Check all Python processes
ps aux | grep python

# Check specifically for bot
ps aux | grep telegram_bot.py

# Check with pgrep
pgrep -af telegram_bot
```

---

## 🔴 Error: "name 're' is not defined"

**Fixed!** The `re` module import was missing. Already added in the latest version.

---

## 🔴 Bot Not Responding

### 1. Check if bot is running
```bash
ps aux | grep telegram_bot.py
```

### 2. Check environment variables
```bash
# Verify .env file exists
cat .env

# Should contain:
# TELEGRAM_BOT_TOKEN=your_token
# GROQ_API_KEY=your_key
```

### 3. Test bot token
```bash
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TELEGRAM_BOT_TOKEN')
print(f'Token loaded: {token[:10]}...' if token else 'Token not found!')
"
```

### 4. Check logs
The bot prints logs to the console. Look for:
- ✅ "Bot started successfully"
- ❌ Error messages
- 📨 "Processing message from..."

---

## 🔴 Groq API Errors

### Rate Limit Exceeded
```
Error: Rate limit exceeded
```

**Solution**: Wait a few minutes or upgrade your Groq API plan.

### Invalid API Key
```
Error: 401 Unauthorized
```

**Solution**: Check your `GROQ_API_KEY` in `.env` file.

### Model Not Found
```
Error: Model not found
```

**Solution**: Update model name in `.env`:
```bash
GROQ_MODEL_NAME=llama-3.3-70b-versatile
```

---

## 🔴 Image Support Not Working

### Check Vision Model
```bash
# In .env, ensure:
GROQ_VISION_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
```

### Test Image Processing
Send an image to the bot with caption. Check logs for:
```
INFO - Processing image from user...
```

---

## 🚀 Proper Bot Startup

### Method 1: Direct Run (Recommended for Testing)
```bash
python3 telegram_bot.py
```
- See logs in real-time
- Easy to stop with Ctrl+C

### Method 2: Background Process
```bash
nohup python3 telegram_bot.py > bot.log 2>&1 &
```
- Runs in background
- Logs saved to `bot.log`
- Stop with: `pkill -f telegram_bot.py`

### Method 3: Using Screen (Recommended for Servers)
```bash
# Start screen session
screen -S miraibot

# Run bot
python3 telegram_bot.py

# Detach: Press Ctrl+A then D

# Reattach later
screen -r miraibot

# Kill session
screen -X -S miraibot quit
```

### Method 4: Using systemd (Production)
Create `/etc/systemd/system/miraibot.service`:
```ini
[Unit]
Description=MiraiAI Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/MiraiAi
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl start miraibot
sudo systemctl enable miraibot
sudo systemctl status miraibot
```

---

## 🔍 Debugging Tips

### Enable Debug Logging
In `telegram_bot.py`, change:
```python
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Changed from INFO
)
```

### Test Groq API Directly
```python
import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv('GROQ_API_KEY')

response = requests.post(
    'https://api.groq.com/openai/v1/chat/completions',
    headers={'Authorization': f'Bearer {api_key}'},
    json={
        'model': 'llama-3.3-70b-versatile',
        'messages': [{'role': 'user', 'content': 'Hello'}]
    }
)
print(response.json())
```

### Check Telegram Bot Connection
```python
import os
from dotenv import load_dotenv
import requests

load_dotenv()
token = os.getenv('TELEGRAM_BOT_TOKEN')

response = requests.get(f'https://api.telegram.org/bot{token}/getMe')
print(response.json())
```

---

## 📝 Common Issues Checklist

- [ ] Only one bot instance is running
- [ ] `.env` file exists with correct tokens
- [ ] Python 3.8+ is installed
- [ ] All dependencies are installed (`pip install -r requirements.txt`)
- [ ] Groq API key is valid
- [ ] Telegram bot token is valid
- [ ] Internet connection is stable
- [ ] No firewall blocking connections

---

## 🆘 Still Having Issues?

1. **Check logs carefully** - Most errors are clearly described
2. **Restart everything** - Stop bot, clear cache, restart
3. **Test components individually** - API, bot token, etc.
4. **Check GitHub issues** - Someone may have had the same problem
5. **Create an issue** with:
   - Error message
   - Steps to reproduce
   - Your environment (OS, Python version)

---

## 📚 Useful Commands

```bash
# View bot logs (if running in background)
tail -f bot.log

# Check bot status
ps aux | grep telegram_bot.py

# Stop all instances
./stop_bot.sh

# Restart bot
./restart_bot.sh

# Test environment
python3 test_bot.py

# Update dependencies
pip install -r requirements.txt --upgrade
```

---

**Last Updated**: October 2025
