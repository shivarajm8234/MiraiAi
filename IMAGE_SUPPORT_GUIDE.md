# 📸 Image Analysis Feature - Mental Health Support

## ✅ What's New

Your MiraiAI bot can now **understand and respond to images** with emotional support context!

## 🎯 Features

### **Vision Model:** 
- `google/gemini-flash-1.5:free` - FREE multimodal AI
- Understands images and provides empathetic responses
- Connects visual content to emotional state

### **What It Can Do:**

1. **Analyze Photos**
   - Recognizes objects, scenes, people, emotions
   - Understands context from the image
   
2. **Emotional Support Based on Images**
   - Responds empathetically to what's shown
   - Connects image to conversation history
   - Provides 3-line supportive responses

3. **Context-Aware**
   - Remembers previous conversation
   - Uses caption if provided
   - Tailored emotional support

## 📱 How Users Can Use It

### **Example 1: Sharing a sad moment**
```
User: [Sends photo of empty room]
Caption: "This was our place"

Bot: I can see this space holds memories for you.
     Empty rooms can feel heavy with what's missing.
     Want to tell me about what this place meant?
```

### **Example 2: Sharing nature for comfort**
```
User: [Sends photo of sunset]
Caption: "Trying to find peace"

Bot: That's a beautiful sunset you're watching.
     Nature can be healing when we're hurting.
     How are you feeling right now?
```

### **Example 3: Self-expression**
```
User: [Sends photo of artwork/drawing]
Caption: "Made this today"

Bot: I can see you put emotion into this.
     Creating art is a powerful way to express feelings.
     What were you feeling while making it?
```

### **Example 4: Sharing difficult moments**
```
User: [Sends photo of hospital/medical setting]

Bot: I can see you're in a challenging place.
     Medical situations can be scary and overwhelming.
     I'm here for you. How are you holding up?
```

## 🔧 Technical Details

### **Model Used:**
- **google/gemini-flash-1.5:free**
- FREE vision model from Google
- Fast and accurate image understanding
- Emotional intelligence in responses

### **Response Format:**
- 3 short lines (25-35 words)
- Empathetic and supportive
- Connects image to emotional state
- Uses conversation context

### **Privacy:**
- Images processed via OpenRouter API
- Not stored permanently
- Only used for immediate response
- Conversation context maintained

## 🎨 Best Use Cases

✅ **Sharing moments of sadness** - Empty places, memories
✅ **Nature for healing** - Sunsets, landscapes, peaceful scenes
✅ **Self-expression** - Art, drawings, creative work
✅ **Current situations** - Where they are, what they're experiencing
✅ **Emotional triggers** - Things that make them feel certain ways

## ⚠️ What It Won't Do

❌ Medical diagnosis from images
❌ Identify specific people (privacy)
❌ Give medical advice
❌ Replace professional help

## 🚀 How to Test

1. Open your bot in Telegram
2. Send any photo
3. Optionally add a caption
4. Bot will analyze and respond empathetically

### **Test Examples:**

**Send a photo of:**
- A place that makes you sad
- Something that brings you peace
- Art you created
- Your current surroundings
- Something meaningful to you

**With captions like:**
- "This is where we used to go"
- "Feeling lost today"
- "Made this when I was angry"
- "This helps me calm down"
- "Missing this"

## 📊 Free Vision Models Available

You can change the vision model in `.env`:

```env
# Current (Recommended - Fast & Free)
VISION_MODEL_NAME=google/gemini-flash-1.5:free

# Alternative Free Options:
# VISION_MODEL_NAME=google/gemini-2.0-flash-exp:free
# VISION_MODEL_NAME=meta-llama/llama-3.2-11b-vision-instruct:free
```

## 💡 Tips for Users

1. **Add captions** - Helps bot understand context better
2. **Share what matters** - Photos of meaningful places/things
3. **Express yourself** - Art, drawings, creative work
4. **Current moments** - Where you are, what you're seeing
5. **Memory triggers** - Things that bring up emotions

---

## ✨ Summary

Your bot now provides **visual emotional support**! Users can share:
- 📷 Photos of meaningful places
- 🎨 Creative expressions
- 🌅 Calming scenes
- 💔 Difficult moments
- 🏥 Current situations

And receive **empathetic, context-aware responses** in 3 short, supportive lines.

**All completely FREE using Google's Gemini Flash vision model!** 🚀
