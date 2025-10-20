# 🚀 FREE Deployment Guide - MiraiAI Bot

## ✅ Deploy on Render (100% FREE Forever!)

**Render is the ONLY deployment method for this bot - it's completely FREE!**

### ✅ Option 1: Render (RECOMMENDED - Easiest)

**Why Render?**
- ✅ 100% FREE forever
- ✅ No credit card required
- ✅ Always running (no cold starts)
- ✅ Easy GitHub integration
- ✅ Auto-deploy on push

**Steps:**

1. **Push code to GitHub:**
   ```bash
   cd /home/kiyotoka/Desktop/MiraiAi
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   # Create repo on GitHub first, then:
   git remote add origin https://github.com/YOUR_USERNAME/MiraiAI.git
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to: https://render.com
   - Sign up (free, no credit card)
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Render will auto-detect `render.yaml`
   - Click "Create Web Service"
   - **Done!** Bot will be running in 2-3 minutes

3. **Check logs:**
   - Click on your service
   - Go to "Logs" tab
   - See bot running!

---

### ✅ Option 2: Railway (Also Great)

**Why Railway?**
- ✅ $5 FREE credit/month
- ✅ No credit card for trial
- ✅ Very fast deployment
- ✅ Great dashboard

**Steps:**

1. **Install Railway CLI:**
   ```bash
   npm i -g @railway/cli
   ```

2. **Deploy:**
   ```bash
   cd /home/kiyotoka/Desktop/MiraiAi
   railway login
   railway init
   railway up
   ```

3. **Set environment variables:**
   - Go to Railway dashboard
   - Click your project
   - Go to "Variables" tab
   - Add:
     - `TELEGRAM_BOT_TOKEN`
     - `GROQ_API_KEY`
     - `GROQ_MODEL_NAME`
     - `GROQ_VISION_MODEL`

---

### ✅ Option 3: Fly.io (Good Alternative)

**Why Fly.io?**
- ✅ FREE tier (3 VMs)
- ✅ Always running
- ✅ Global deployment

**Steps:**

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Deploy:**
   ```bash
   cd /home/kiyotoka/Desktop/MiraiAi
   fly auth signup  # or fly auth login
   fly launch
   fly secrets set TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
   fly secrets set GROQ_API_KEY=YOUR_GROQ_API_KEY
   fly secrets set GROQ_MODEL_NAME=llama-3.3-70b-versatile
   fly secrets set GROQ_VISION_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
   fly deploy
   ```

---

## 🏆 My Recommendation: Use Render

**Render is the easiest and most reliable FREE option!**

### Quick Render Setup (5 minutes):

1. **Create GitHub repo** (if you don't have one)
2. **Push your code** to GitHub
3. **Go to render.com** and sign up
4. **Connect GitHub** and select your repo
5. **Click Deploy** - Done!

The `render.yaml` file I created will handle everything automatically.

---

## 📊 Comparison

| Platform | Free Tier | Credit Card | Ease | Always On |
|----------|-----------|-------------|------|-----------|
| **Render** | ✅ Forever | ❌ No | ⭐⭐⭐⭐⭐ | ✅ Yes |
| **Railway** | ✅ $5/month | ❌ No | ⭐⭐⭐⭐ | ✅ Yes |
| **Fly.io** | ✅ 3 VMs | ⚠️ Yes | ⭐⭐⭐ | ✅ Yes |
| **Heroku** | ❌ Paid | ✅ Yes | ⭐⭐⭐⭐ | ✅ Yes |
| **Firebase** | ⚠️ Limited | ⚠️ Yes | ⭐⭐ | ❌ No |

---

## 🎯 Next Steps

**Choose Render** and follow these steps:

1. Create GitHub account (if needed)
2. Push code to GitHub
3. Sign up on Render.com
4. Connect GitHub repo
5. Deploy!

Your bot will be running 24/7 for FREE! 🚀

---

## 💡 Tips

- **Render free tier:** Bot sleeps after 15 min inactivity, but wakes instantly
- **To keep always active:** Add a health check endpoint (I can help with this)
- **Logs:** Available in Render dashboard
- **Updates:** Just push to GitHub, auto-deploys!

---

## 🆘 Need Help?

Let me know which platform you choose and I'll guide you through it! 💙
