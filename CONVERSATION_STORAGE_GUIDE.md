# Conversation Storage Guide

This guide shows how to store user conversations using free cloud services.

## 🎯 Best Free Options

### 1. **MongoDB Atlas (Recommended)** ⭐
- **Free Tier**: 512MB storage
- **Perfect for**: Structured conversation data
- **Pros**: Easy to use, scalable, good for analytics
- **Setup Time**: 5 minutes

### 2. **Supabase (PostgreSQL)**
- **Free Tier**: 500MB database, 1GB file storage
- **Perfect for**: Relational data with real-time features
- **Pros**: Built-in authentication, real-time subscriptions
- **Setup Time**: 5 minutes

### 3. **Google Sheets API**r
- **Free Tier**: Unlimited (with rate limits)
- **Perfect for**: Simple logging, easy viewing
- **Pros**: No setup, view in browser, export to Excel
- **Setup Time**: 2 minutes

### 4. **JSON Files + GitHub**
- **Free Tier**: Unlimited (for small files)
- **Perfect for**: Backup, version control
- **Pros**: Simple, no external dependencies
- **Setup Time**: 1 minute

### 5. **Firebase Firestore**
- **Free Tier**: 1GB storage, 50K reads/day
- **Perfect for**: Real-time sync, mobile apps
- **Pros**: Google integration, real-time updates
- **Setup Time**: 5 minutes

---

## 🚀 Quick Implementation

### Option 1: MongoDB Atlas (Best Choice)

#### Setup MongoDB Atlas

1. **Create Account**: https://www.mongodb.com/cloud/atlas/register
2. **Create Free Cluster** (M0 tier - 512MB)
3. **Get Connection String**:
   - Click "Connect" → "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your password

#### Install Dependencies

```bash
pip install pymongo dnspython
```

#### Add to `.env`

```bash
MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

#### Implementation Code

```python
# Add to telegram_bot.py

from pymongo import MongoClient
from datetime import datetime
import os

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI")
mongo_client = MongoClient(MONGODB_URI) if MONGODB_URI else None
db = mongo_client["miraibot"] if mongo_client else None
conversations_collection = db["conversations"] if db else None

def save_conversation(user_id: int, username: str, message: str, bot_response: str):
    """Save conversation to MongoDB"""
    if not conversations_collection:
        return
    
    try:
        conversation_data = {
            "user_id": user_id,
            "username": username,
            "timestamp": datetime.utcnow(),
            "user_message": message,
            "bot_response": bot_response,
            "message_length": len(message),
            "response_length": len(bot_response)
        }
        conversations_collection.insert_one(conversation_data)
        logger.info(f"Saved conversation for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to save conversation: {e}")

# In your message handler, add:
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ... existing code ...
    
    # Get bot response
    bot_response = await get_ai_response(user_message, user_id)
    
    # Save to database
    save_conversation(
        user_id=user_id,
        username=update.effective_user.username or "Unknown",
        message=user_message,
        bot_response=bot_response
    )
    
    # Send response
    await update.message.reply_text(bot_response)
```

#### Query Conversations

```python
# Get all conversations for a user
def get_user_conversations(user_id: int, limit: int = 50):
    if not conversations_collection:
        return []
    
    return list(conversations_collection.find(
        {"user_id": user_id}
    ).sort("timestamp", -1).limit(limit))

# Get conversation statistics
def get_conversation_stats():
    if not conversations_collection:
        return {}
    
    return {
        "total_conversations": conversations_collection.count_documents({}),
        "unique_users": len(conversations_collection.distinct("user_id")),
        "avg_message_length": conversations_collection.aggregate([
            {"$group": {"_id": None, "avg": {"$avg": "$message_length"}}}
        ]).next()["avg"]
    }
```

---

### Option 2: Google Sheets (Simplest)

#### Setup Google Sheets API

1. **Create Project**: https://console.cloud.google.com/
2. **Enable Google Sheets API**
3. **Create Service Account** → Download JSON key
4. **Share Sheet** with service account email

#### Install Dependencies

```bash
pip install gspread oauth2client
```

#### Implementation Code

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Setup Google Sheets
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
sheets_client = gspread.authorize(creds)

# Open or create spreadsheet
sheet = sheets_client.open("MiraiBot Conversations").sheet1

# Set headers if new
if sheet.row_count == 0:
    sheet.append_row([
        "Timestamp", "User ID", "Username", 
        "User Message", "Bot Response", "Message Length"
    ])

def save_to_sheets(user_id: int, username: str, message: str, bot_response: str):
    """Save conversation to Google Sheets"""
    try:
        row = [
            datetime.now().isoformat(),
            user_id,
            username,
            message,
            bot_response,
            len(message)
        ]
        sheet.append_row(row)
        logger.info(f"Saved to Google Sheets: User {user_id}")
    except Exception as e:
        logger.error(f"Failed to save to sheets: {e}")
```

---

### Option 3: Supabase (PostgreSQL)

#### Setup Supabase

1. **Create Account**: https://supabase.com/
2. **Create Project** (free tier)
3. **Get API Keys** from Settings → API
4. **Create Table**:

```sql
CREATE TABLE conversations (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    username TEXT,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    message_length INT,
    response_length INT
);

-- Create index for faster queries
CREATE INDEX idx_user_id ON conversations(user_id);
CREATE INDEX idx_timestamp ON conversations(timestamp DESC);
```

#### Install Dependencies

```bash
pip install supabase
```

#### Add to `.env`

```bash
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your_anon_key
```

#### Implementation Code

```python
from supabase import create_client, Client
from datetime import datetime

# Supabase connection
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL else None

def save_to_supabase(user_id: int, username: str, message: str, bot_response: str):
    """Save conversation to Supabase"""
    if not supabase:
        return
    
    try:
        data = {
            "user_id": user_id,
            "username": username,
            "user_message": message,
            "bot_response": bot_response,
            "message_length": len(message),
            "response_length": len(bot_response),
            "timestamp": datetime.utcnow().isoformat()
        }
        supabase.table("conversations").insert(data).execute()
        logger.info(f"Saved to Supabase: User {user_id}")
    except Exception as e:
        logger.error(f"Failed to save to Supabase: {e}")

# Query conversations
def get_user_history(user_id: int, limit: int = 50):
    if not supabase:
        return []
    
    response = supabase.table("conversations")\
        .select("*")\
        .eq("user_id", user_id)\
        .order("timestamp", desc=True)\
        .limit(limit)\
        .execute()
    
    return response.data
```

---

### Option 4: Local JSON Files (Backup)

#### Simple Implementation

```python
import json
from datetime import datetime
from pathlib import Path

CONVERSATIONS_DIR = Path("conversations_backup")
CONVERSATIONS_DIR.mkdir(exist_ok=True)

def save_to_json(user_id: int, username: str, message: str, bot_response: str):
    """Save conversation to local JSON file"""
    try:
        # Create user-specific file
        user_file = CONVERSATIONS_DIR / f"user_{user_id}.json"
        
        # Load existing conversations
        if user_file.exists():
            with open(user_file, 'r', encoding='utf-8') as f:
                conversations = json.load(f)
        else:
            conversations = []
        
        # Add new conversation
        conversations.append({
            "timestamp": datetime.now().isoformat(),
            "username": username,
            "user_message": message,
            "bot_response": bot_response
        })
        
        # Save back
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(conversations, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved to JSON: User {user_id}")
    except Exception as e:
        logger.error(f"Failed to save to JSON: {e}")

# Export all conversations
def export_all_conversations():
    """Export all conversations to single file"""
    all_conversations = []
    
    for user_file in CONVERSATIONS_DIR.glob("user_*.json"):
        with open(user_file, 'r', encoding='utf-8') as f:
            user_data = json.load(f)
            user_id = user_file.stem.replace("user_", "")
            all_conversations.extend([
                {**conv, "user_id": user_id} for conv in user_data
            ])
    
    # Save to export file
    export_file = CONVERSATIONS_DIR / f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(export_file, 'w', encoding='utf-8') as f:
        json.dump(all_conversations, f, indent=2, ensure_ascii=False)
    
    return export_file
```

---

## 🔒 Privacy & Security Considerations

### Important Notes

1. **User Consent**: Inform users that conversations are stored
2. **Data Anonymization**: Consider hashing user IDs
3. **Sensitive Data**: Don't store personal information (phone, address, etc.)
4. **Retention Policy**: Delete old conversations after X days
5. **Encryption**: Encrypt sensitive fields

### Privacy-Friendly Implementation

```python
import hashlib

def anonymize_user_id(user_id: int) -> str:
    """Hash user ID for privacy"""
    return hashlib.sha256(str(user_id).encode()).hexdigest()[:16]

def filter_sensitive_data(message: str) -> str:
    """Remove sensitive information from messages"""
    import re
    
    # Remove phone numbers
    message = re.sub(r'\b\d{10}\b', '[PHONE]', message)
    
    # Remove emails
    message = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', message)
    
    # Remove credit card numbers
    message = re.sub(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', '[CARD]', message)
    
    return message

def save_conversation_private(user_id: int, username: str, message: str, bot_response: str):
    """Save conversation with privacy protection"""
    # Anonymize user ID
    anon_id = anonymize_user_id(user_id)
    
    # Filter sensitive data
    clean_message = filter_sensitive_data(message)
    clean_response = filter_sensitive_data(bot_response)
    
    # Save with anonymized data
    save_conversation(anon_id, "Anonymous", clean_message, clean_response)
```

---

## 📊 Analytics Dashboard

### Query Examples (MongoDB)

```python
from datetime import datetime, timedelta

def get_analytics():
    """Get conversation analytics"""
    if not conversations_collection:
        return {}
    
    # Last 7 days
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    return {
        # Total conversations
        "total": conversations_collection.count_documents({}),
        
        # This week
        "this_week": conversations_collection.count_documents({
            "timestamp": {"$gte": week_ago}
        }),
        
        # Unique users
        "unique_users": len(conversations_collection.distinct("user_id")),
        
        # Average message length
        "avg_message_length": list(conversations_collection.aggregate([
            {"$group": {"_id": None, "avg": {"$avg": "$message_length"}}}
        ]))[0]["avg"],
        
        # Most active users
        "top_users": list(conversations_collection.aggregate([
            {"$group": {"_id": "$user_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ])),
        
        # Messages per day
        "messages_per_day": list(conversations_collection.aggregate([
            {"$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": -1}},
            {"$limit": 30}
        ]))
    }
```

---

## 🎯 Recommended Setup

### For Most Users: MongoDB Atlas

**Why?**
- ✅ Free 512MB storage (thousands of conversations)
- ✅ Easy to query and analyze
- ✅ Scalable when you need more
- ✅ Built-in backup and security
- ✅ Works with analytics tools

### Complete Implementation

```python
# Add to telegram_bot.py after imports

from pymongo import MongoClient
from datetime import datetime
import hashlib

# MongoDB setup
MONGODB_URI = os.getenv("MONGODB_URI")
mongo_client = MongoClient(MONGODB_URI) if MONGODB_URI else None
db = mongo_client["miraibot"] if mongo_client else None
conversations_collection = db["conversations"] if db else None

def save_conversation_to_db(user_id: int, username: str, message: str, bot_response: str):
    """Save conversation with privacy protection"""
    if not conversations_collection:
        logger.warning("MongoDB not configured, skipping save")
        return
    
    try:
        # Anonymize if needed
        anon_id = hashlib.sha256(str(user_id).encode()).hexdigest()[:16]
        
        conversation_data = {
            "user_id_hash": anon_id,
            "username": username or "Anonymous",
            "timestamp": datetime.utcnow(),
            "user_message": message[:500],  # Limit length
            "bot_response": bot_response[:1000],
            "message_length": len(message),
            "response_length": len(bot_response),
            "language": "en"  # Detect language if needed
        }
        
        conversations_collection.insert_one(conversation_data)
        logger.info(f"✅ Saved conversation for user {anon_id[:8]}...")
        
    except Exception as e:
        logger.error(f"❌ Failed to save conversation: {e}")

# In your handle_message function, add:
# save_conversation_to_db(user_id, username, user_message, bot_response)
```

---

## 📝 Update `.env` File

```bash
# Add one of these based on your choice:

# Option 1: MongoDB Atlas
MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority

# Option 2: Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your_anon_key

# Option 3: Google Sheets (use credentials.json file instead)
```

---

## 🔄 Backup Strategy

### Automatic Daily Backup

```python
import schedule
import time

def backup_conversations():
    """Export conversations daily"""
    export_file = export_all_conversations()
    logger.info(f"Backup created: {export_file}")

# Schedule daily backup at 2 AM
schedule.every().day.at("02:00").do(backup_conversations)

# Run in background thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

# Start scheduler
threading.Thread(target=run_scheduler, daemon=True).start()
```

---

## 📚 Next Steps

1. **Choose your storage solution** (MongoDB recommended)
2. **Set up account and get credentials**
3. **Add credentials to `.env`**
4. **Install required packages**
5. **Add save function to bot code**
6. **Test with a few messages**
7. **Set up analytics dashboard** (optional)

---

**Need help?** See [BOT_TROUBLESHOOTING.md](BOT_TROUBLESHOOTING.md)
