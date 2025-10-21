# Railway CLI Deployment (Alternative Method)

If the web interface gives workspace errors, use the CLI:

## 1. Install Railway CLI

```bash
# Using npm (if you have Node.js)
npm i -g @railway/cli

# Or using curl (Linux/Mac)
curl -fsSL https://railway.app/install.sh | sh
```

## 2. Login to Railway

```bash
railway login
```

This will open your browser to authenticate.

## 3. Initialize Project

```bash
cd /home/kiyotoka/Desktop/MiraiAi
railway init
```

This will:
- Create a new project
- Link your local directory to Railway
- Automatically create workspace if needed

## 4. Add Environment Variables

```bash
railway variables set TELEGRAM_BOT_TOKEN="your_bot_token_here"
railway variables set GROQ_API_KEY="your_groq_api_key_here"
railway variables set GROQ_MODEL_NAME="llama-3.3-70b-versatile"
railway variables set GROQ_VISION_MODEL="meta-llama/llama-4-scout-17b-16e-instruct"
railway variables set PORT="8080"
```

## 5. Deploy

```bash
railway up
```

This will:
- Upload your code
- Install dependencies
- Start your bot

## 6. Check Status

```bash
# View logs
railway logs

# Check service status
railway status

# Open dashboard
railway open
```

## Done! 🎉

Your bot should now be running on Railway.

## Useful Commands

```bash
# View logs in real-time
railway logs --follow

# Restart service
railway restart

# Link to existing project
railway link

# Unlink project
railway unlink
```

## Troubleshooting

### Command not found?
Make sure Railway CLI is in your PATH:
```bash
export PATH="$HOME/.railway/bin:$PATH"
```

### Authentication issues?
```bash
railway logout
railway login
```

### Need to change project?
```bash
railway unlink
railway link
```
