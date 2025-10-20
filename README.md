# 🧠 Mental Health Support Telegram Bot

A professional, empathetic mental health support chatbot powered by fine-tuned **Llama 3.1 8B** with built-in crisis intervention protocols. Designed to provide 24/7 emotional support while maintaining strict ethical boundaries.

## ✨ Features

- **🤖 AI-Powered Empathy**: Fine-tuned Llama 3.1 8B for compassionate, emotion-aware responses
- **🆘 Crisis Detection**: Automatic detection of self-harm/suicidal language with immediate intervention
- **💬 Contextual Memory**: Maintains short-term conversation context (last 8 messages)
- **🔒 Privacy-First**: No permanent message logging, all processing in-memory
- **⚡ Optimized Performance**: 4-bit quantization for efficient GPU usage
- **📱 Telegram Integration**: Seamless chat experience with typing indicators
- **🌍 Resource Library**: Comprehensive crisis helplines and mental health resources

## 🚨 Important Disclaimer

This bot provides **emotional support only** and is **NOT**:
- A replacement for professional mental health care
- A source of medical, legal, or financial advice
- An emergency service

**In crisis situations, always contact emergency services (911) or crisis helplines immediately.**

---

## 📋 Prerequisites

- **Python 3.9+**
- **CUDA-capable GPU** (recommended) or CPU with sufficient RAM
- **Telegram Bot Token** (from [@BotFather](https://t.me/botfather))
- **Hugging Face Account** (for model access)
- **Linux Server** or cloud instance (for 24/7 deployment)

---

## 🚀 Quick Start

### 1. Clone or Download the Project

```bash
cd /path/to/your/project
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Optional: Install Unsloth for optimized fine-tuning**
```bash
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
nano .env  # or use your preferred editor
```

**Required variables:**
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz  # From @BotFather
MODEL_PATH=unsloth/Llama-3.1-8B-Instruct                 # Or your local model path
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx                # From huggingface.co/settings/tokens
ADMIN_CHAT_ID=123456789                                  # Optional: Your Telegram chat ID
```

### 5. Get Your Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow the prompts
3. Copy the bot token provided
4. Paste it into your `.env` file

### 6. Get Your Hugging Face Token

1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Create a new token with **read** access
3. Copy and paste into your `.env` file

### 7. Run the Bot

```bash
python telegram_bot.py
```

You should see:
```
INFO - Starting Mental Health Support Bot...
INFO - Loading model from unsloth/Llama-3.1-8B-Instruct...
INFO - Model loaded successfully!
INFO - Bot is running! Press Ctrl+C to stop.
```

### 8. Test Your Bot

1. Open Telegram and search for your bot by username
2. Send `/start` to begin
3. Try sending a message like "I'm feeling anxious today"

---

## 🎯 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message with disclaimer and introduction |
| `/help` | Show available commands and usage instructions |
| `/resources` | Display crisis helplines and mental health resources |

---

## 🔧 Configuration Options

### Model Selection

**Option 1: Use Pre-trained Model (Default)**
```env
MODEL_PATH=unsloth/Llama-3.1-8B-Instruct
```

**Option 2: Use Your Fine-Tuned Model**
```env
MODEL_PATH=/path/to/your/fine-tuned-model
```

**Option 3: Use Different Hugging Face Model**
```env
MODEL_PATH=meta-llama/Llama-3.1-8B-Instruct
```

### Memory Configuration

Edit `telegram_bot.py` to adjust conversation memory:
```python
MAX_MEMORY_LENGTH = 8  # Number of messages to remember (default: 8)
```

### Crisis Detection Patterns

Add custom crisis detection patterns in `telegram_bot.py`:
```python
CRISIS_PATTERNS = [
    r'\b(kill|hurt|harm)\s+(myself|me)\b',
    r'\bsuicid(e|al)\b',
    # Add your patterns here
]
```

---

## 🌐 24/7 Deployment

### Option 1: Systemd Service (Linux)

1. **Create service file:**

```bash
sudo nano /etc/systemd/system/mental-health-bot.service
```

2. **Add configuration:**

```ini
[Unit]
Description=Mental Health Support Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/MiraiAi
Environment="PATH=/path/to/MiraiAi/venv/bin"
ExecStart=/path/to/MiraiAi/venv/bin/python telegram_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. **Enable and start service:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable mental-health-bot
sudo systemctl start mental-health-bot
```

4. **Check status:**

```bash
sudo systemctl status mental-health-bot
sudo journalctl -u mental-health-bot -f  # View logs
```

### Option 2: Screen/Tmux (Quick Method)

```bash
# Using screen
screen -S mental-health-bot
python telegram_bot.py
# Press Ctrl+A, then D to detach

# Reattach later
screen -r mental-health-bot
```

```bash
# Using tmux
tmux new -s mental-health-bot
python telegram_bot.py
# Press Ctrl+B, then D to detach

# Reattach later
tmux attach -t mental-health-bot
```

### Option 3: Render.com Deployment

1. **Create `render.yaml`:**

```yaml
services:
  - type: web
    name: mental-health-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python telegram_bot.py
    envVars:
      - key: TELEGRAM_BOT_TOKEN
        sync: false
      - key: MODEL_PATH
        value: unsloth/Llama-3.1-8B-Instruct
      - key: HF_TOKEN
        sync: false
```

2. **Push to GitHub and connect to Render**
3. **Add environment variables in Render dashboard**

---

## 🛡️ Crisis Intervention Protocol

When crisis language is detected:

1. **Immediate Response**: Bot sends empathetic crisis intervention message with helplines
2. **Admin Alert**: If `ADMIN_CHAT_ID` is configured, admin receives notification
3. **No AI Response**: Crisis messages bypass AI to ensure immediate, appropriate response

**Crisis Detection Triggers:**
- Self-harm language
- Suicidal ideation
- Expressions of wanting to die
- No reason to live statements

---

## 🧪 Testing

### Test Crisis Detection

Send these messages to verify crisis protocol:
```
"I want to hurt myself"
"I don't want to live anymore"
```

Expected: Immediate crisis response with helplines

### Test Normal Conversation

```
"I'm feeling really anxious today"
"I can't stop worrying about everything"
```

Expected: Empathetic AI-generated response

### Test Fallback Responses

Stop the bot, comment out model loading, and restart:
```python
# load_model()  # Comment this line
```

Expected: Bot uses fallback empathetic responses

---

## 📊 System Requirements

### Minimum (CPU Mode)
- **RAM**: 16GB
- **Storage**: 20GB
- **CPU**: 4+ cores

### Recommended (GPU Mode)
- **GPU**: NVIDIA GPU with 8GB+ VRAM (RTX 3060 or better)
- **RAM**: 16GB
- **Storage**: 20GB
- **CUDA**: 11.8+

### Cloud Options
- **AWS**: g4dn.xlarge or larger
- **Google Cloud**: n1-standard-4 with T4 GPU
- **Render**: Pro plan with GPU support

---

## 🐛 Troubleshooting

### Bot doesn't respond

**Check logs:**
```bash
# If using systemd
sudo journalctl -u mental-health-bot -n 50

# If running directly
# Check terminal output
```

**Common issues:**
- Invalid bot token → Verify in `.env`
- Model loading failed → Check HF_TOKEN and MODEL_PATH
- Network issues → Verify internet connection

### Model loading fails

**Error: "CUDA out of memory"**
```python
# Reduce batch size or use CPU
device_map="cpu"  # In load_model() function
```

**Error: "Token is required"**
```bash
# Verify HF_TOKEN is set
echo $HF_TOKEN
```

### Crisis detection not working

**Verify patterns in logs:**
```python
# Add debug logging
logger.info(f"Checking crisis patterns for: {message}")
```

---

## 🔐 Security & Privacy

- ✅ **No permanent storage**: Messages processed in-memory only
- ✅ **No database**: Conversation memory cleared on restart
- ✅ **Environment variables**: Sensitive tokens stored securely
- ✅ **Admin alerts**: Optional crisis notifications to designated admin
- ✅ **No third-party logging**: All processing local

---

## 📝 Customization

### Modify System Prompt

Edit the system prompt in `telegram_bot.py`:
```python
system_prompt = (
    "You are a compassionate mental health support companion..."
    # Customize here
)
```

### Adjust Response Length

```python
outputs = model.generate(
    inputs,
    max_new_tokens=150,  # Increase for longer responses
    temperature=0.7,     # Lower for more focused responses
    top_p=0.9,
)
```

### Add Custom Commands

```python
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Your custom response")

# Register handler
application.add_handler(CommandHandler("custom", custom_command))
```

---

## 📚 Resources

### Crisis Helplines
- **988 Suicide & Crisis Lifeline (US)**: Call/Text 988
- **Crisis Text Line**: Text HOME to 741741
- **International**: https://findahelpline.com

### Documentation
- [python-telegram-bot](https://docs.python-telegram-bot.org/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [Unsloth](https://github.com/unslothai/unsloth)

---

## 🤝 Contributing

This is a mental health support tool. Contributions should:
- Maintain empathetic, non-judgmental tone
- Follow crisis intervention best practices
- Preserve privacy and security standards
- Include appropriate disclaimers

---

## ⚖️ License

This project is provided as-is for educational and support purposes. Always consult licensed mental health professionals for clinical care.

---

## 🙏 Acknowledgments

- **Llama 3.1** by Meta AI
- **Unsloth** for optimized fine-tuning
- **python-telegram-bot** community
- Mental health professionals and crisis counselors worldwide

---

## 📧 Support

For technical issues, please check:
1. Logs (`journalctl` or terminal output)
2. Environment variables (`.env` file)
3. Model loading status
4. Network connectivity

**Remember**: This bot is a support tool, not a replacement for professional help. If you or someone you know is in crisis, please contact emergency services immediately.

---

**Built with 💙 to support mental wellness**
