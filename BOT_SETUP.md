# 🤖 MiraiAI Bot Configuration Guide

## Bot Profile Setup via @BotFather

### 1. Set Bot Name
```
/setname
@your_bot_username
MiraiAI
```

### 2. Set About (Short Description - 120 chars)
```
/setabouttext
@your_bot_username
Your compassionate AI companion for mental and emotional health support. Available 24/7 to listen and help.
```

### 3. Set Description (Long Description - 512 chars)
```
/setdescription
@your_bot_username
Welcome to MiraiAI - Your Mental Health Support Companion 🌟

I'm here to provide empathetic emotional support whenever you need it. This is a safe, judgment-free space where you can share your feelings and thoughts.

What I offer:
• Compassionate listening and emotional validation
• Support for anxiety, stress, sadness, and difficult emotions
• Crisis intervention with immediate helpline resources
• 24/7 availability

Important: I provide emotional support, not medical advice. In crisis situations, please contact emergency services immediately.

Let's talk. I'm here for you. 💙
```

### 4. Set Commands
```
/setcommands
@your_bot_username

start - Welcome message and introduction
help - Show available commands and how to use the bot
resources - Crisis helplines and mental health resources
```

### 5. Set Bot Picture (Profile Photo)
```
/setuserpic
@your_bot_username
[Upload a calming, professional image - suggest a brain/heart icon or peaceful colors]
```

### 6. Set Privacy Policy (Optional but Recommended)
```
/setprivacy
@your_bot_username

Privacy Policy for MiraiAI Bot:

1. Data Collection:
   - We process messages in-memory only for conversation context
   - No messages are permanently stored or logged
   - Conversation history is cleared when the bot restarts

2. Data Usage:
   - Messages are sent to OpenRouter API for AI processing
   - Used solely to provide emotional support responses
   - Not shared with third parties except the AI service provider

3. Data Retention:
   - Temporary: Conversation context kept in memory during active session
   - Automatic deletion when bot restarts or after inactivity
   - No long-term storage or databases

4. User Rights:
   - You can delete your conversation anytime by restarting the chat
   - No personal data is retained after session ends

5. Security:
   - All communications encrypted via Telegram
   - API calls use secure HTTPS connections

6. Crisis Situations:
   - Crisis alerts may be sent to designated admin for safety monitoring
   - This is to ensure user safety in emergency situations

For questions: Contact bot administrator

Last updated: October 2025
```

### 7. Set Inline Mode (Optional)
```
/setinline
@your_bot_username
disabled
```

### 8. Set Join Groups (Optional)
```
/setjoingroups
@your_bot_username
disabled
```

---

## Quick Setup Commands Summary

Open Telegram → Search @BotFather → Send these commands:

```
/setname
MiraiAI

/setabouttext
Your compassionate AI companion for mental and emotional health support. Available 24/7 to listen and help.

/setdescription
[Copy the long description above]

/setcommands
start - Welcome message and introduction
help - Show available commands and how to use the bot
resources - Crisis helplines and mental health resources

/setuserpic
[Upload image]

/setjoingroups
disabled

/setinline
disabled
```

---

## Recommended Bot Picture Ideas

1. **Brain + Heart Icon** - Symbolizes mental health and emotional care
2. **Peaceful Colors** - Soft blues, purples, or greens
3. **Abstract Calming Design** - Waves, circles, or gentle patterns
4. **Professional Logo** - "MiraiAI" text with calming background

**Image Requirements:**
- Format: JPG or PNG
- Size: 512x512 pixels recommended
- Professional and calming appearance
- No text clutter

---

## Testing Your Bot Profile

After setup, test by:
1. Searching for your bot in Telegram
2. Check the profile shows correct name and picture
3. Read the description before starting chat
4. Verify commands appear in the menu (/)
5. Send /start to test welcome message

---

## Current Bot Status

✅ **Bot Token:** Configured
✅ **OpenRouter API:** Configured  
✅ **Model:** meta-llama/llama-3.2-3b-instruct:free
✅ **Bot Running:** Yes
⏳ **Profile Setup:** Pending (use commands above)
⏳ **Bot Picture:** Pending upload
⏳ **Commands:** Pending configuration

---

**Next Steps:**
1. Open Telegram
2. Search for @BotFather
3. Use the commands above to configure your bot
4. Upload a professional bot picture
5. Test the bot profile
