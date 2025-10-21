# 🚂 Railway.app Deployment Guide

## Prerequisites
- GitHub account
- Railway.app account (sign up at https://railway.app)
- Your code pushed to GitHub

## Step-by-Step Deployment

### 1. Push Your Code to GitHub
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### 2. Deploy on Railway

1. **Go to Railway.app**
   - Visit: https://railway.app
   - Click "Start a New Project"

2. **Deploy from GitHub**
   - Click "Deploy from GitHub repo"
   - Select your repository: `shivarajm8234/MiraiAi`
   - Click "Deploy Now"

3. **Add Environment Variables**
   - Click on your deployed service
   - Go to "Variables" tab
   - Add the following variables:

   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   GROQ_API_KEY=your_primary_groq_api_key_here
   GROQ_API_KEY_1=your_backup_groq_key_1_here
   GROQ_API_KEY_2=your_backup_groq_key_2_here
   GROQ_MODEL_NAME=llama-3.3-70b-versatile
   GROQ_VISION_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
   ADMIN_CHAT_ID=your_telegram_chat_id (optional)
   PORT=8080
   ```

   **Note**: The bot uses 3 API keys for automatic failover when rate limits are hit. This gives you 300,000 tokens/day total (100k per key).

4. **Deploy**
   - Railway will automatically detect Python and install dependencies
   - It will use the `Procfile` to start your bot
   - Wait for deployment to complete (usually 2-3 minutes)

### 3. Generate Public URL for Website

1. **In Railway Dashboard:**
   - Click on your deployed service
   - Go to "Settings" tab
   - Scroll to "Networking" section
   - Click "Generate Domain"
   - Railway will create a public URL like: `your-app.up.railway.app`

2. **Your website will be live at:**
   - `https://your-app.up.railway.app/` - Main website
   - The Telegram bot runs in the background

### 4. Verify Deployment

1. Check the logs in Railway dashboard
2. Look for: 
   - "✅ Bot is running! Press Ctrl+C to stop."
   - "🌐 Starting web server on port 8080"
3. Test your bot on Telegram
4. Visit your generated Railway URL to see the website

## Important Notes

✅ **What's Included:**
- `Procfile` - Tells Railway how to run your bot
- `railway.json` - Railway configuration
- `runtime.txt` - Python version specification
- `requirements.txt` - All dependencies

✅ **Free Tier:**
- Railway offers $5 free credit per month
- Your bot should run 24/7 within free tier
- Monitor usage in Railway dashboard

✅ **Auto-Deploy:**
- Every push to GitHub will auto-deploy
- Railway rebuilds and restarts automatically

## Troubleshooting

### Bot Not Starting?
1. Check logs in Railway dashboard
2. Verify environment variables are set correctly
3. Ensure `TELEGRAM_BOT_TOKEN` is valid

### Out of Memory?
- Railway free tier has memory limits
- Your bot is lightweight and should be fine

### Need Help?
- Railway docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

## Alternative: Manual Deployment

If you prefer manual control:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to project
railway link

# Deploy
railway up
```

## Monitoring

- **Logs**: View in Railway dashboard
- **Metrics**: CPU, Memory, Network usage
- **Alerts**: Set up in Railway settings

## Cost Estimate

With Railway's free tier ($5/month credit):
- Your bot: ~$2-3/month
- Should run 24/7 within free tier
- Upgrade if needed: $5/month for more resources

---

**Your bot is ready for deployment! 🚀**

Just follow the steps above and your mental health support bot will be live on Railway.
