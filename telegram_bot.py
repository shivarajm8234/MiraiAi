#!/usr/bin/env python3
"""
Mental Health Support Telegram Bot with Groq AI Integration
Provides empathetic, context-aware mental health support
"""

import os
import logging
import base64
import threading
import re
from typing import Dict, List
from collections import defaultdict
from dotenv import load_dotenv
import requests

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Flask for web server
from flask import Flask, send_from_directory

import json
import time

# Google Sheets storage (optional)
sheets_enabled = False
save_to_sheets = None
try:
    from google_sheets_storage import init_sheets_storage, save_conversation as save_to_sheets
    sheets_enabled = True
except ImportError:
    logger = logging.getLogger(__name__)
    logger.warning("⚠️ Google Sheets storage not available. Install: pip install gspread oauth2client")

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")  # Text model
GROQ_VISION_MODEL = os.getenv("GROQ_VISION_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")  # Vision model
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# Conversation memory (user_id -> list of messages)
conversation_memory: Dict[int, List[Dict[str, str]]] = defaultdict(list)
MAX_MEMORY_LENGTH = 16  # Increased to remember more context

# Initialize Google Sheets storage
if sheets_enabled:
    try:
        sheets_storage = init_sheets_storage()
        logger.info("✅ Google Sheets storage initialized")
    except Exception as e:
        logger.warning(f"Google Sheets initialization failed: {e}")
        sheets_enabled = False

# Rate limiting to avoid API throttling
last_request_time: Dict[int, float] = defaultdict(float)
MIN_REQUEST_INTERVAL = 1.0  # Minimum 1 second between requests (Groq is fast!)

# Message buffering to combine rapid messages
user_message_buffer: Dict[int, List[str]] = defaultdict(list)
last_message_time: Dict[int, float] = defaultdict(float)
MESSAGE_WAIT_TIME = 3  # Wait 3 seconds for more messages before responding


def extract_phone_number(text: str) -> str:
    """
    Extract phone number from text
    
    Args:
        text: Message text
        
    Returns:
        Phone number if found, None otherwise
    """
    if not text:
        return None
    
    # Pattern for phone numbers (supports various formats)
    # Examples: +91 9876543210, 9876543210, +1-555-123-4567, (555) 123-4567
    phone_patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # +1-555-123-4567
        r'\+?\d{10,13}',  # +919876543210 or 9876543210
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (555) 123-4567
    ]
    
    for pattern in phone_patterns:
        match = re.search(pattern, text)
        if match:
            phone = match.group(0)
            # Clean up the phone number
            phone = re.sub(r'[-.\s()]', '', phone)
            return phone
    
    return None


# Non-mental health topic patterns (to reject)
OFF_TOPIC_PATTERNS = [
    r'\b(weather|temperature|forecast|rain|snow|sunny)\b',
    r'\b(recipe|cook|food|restaurant|menu)\b',
    r'\b(sports|football|basketball|cricket|soccer|match|game score)\b',
    r'\b(movie|film|tv show|series|netflix|watch)\b',
    r'\b(math|calculate|equation|solve|formula)\b',
    r'\b(code|programming|python|javascript|html|css)\b',
    r'\b(news|politics|election|president|government)\b',
    r'\b(stock|market|invest|crypto|bitcoin|trading)\b',
    r'\b(translate|translation|language|dictionary)\b',
    r'\b(history|historical|ancient|war|battle)\b',
    r'\b(science|physics|chemistry|biology|experiment)\b',
    r'\b(geography|capital|country|continent|ocean)\b',
    r'\b(shopping|buy|purchase|amazon|store)\b',
    r'\b(travel|vacation|hotel|flight|booking)\b',
    r'(bought.*car|red car|blue car|what color)',  # Riddles/puzzles about objects
    r'(riddle|puzzle|brain teaser|logic problem)',  # Explicit riddles
]

# Mental health related keywords (to allow)
MENTAL_HEALTH_KEYWORDS = [
    'anxious', 'anxiety', 'stress', 'worried', 'nervous', 'panic',
    'sad', 'depressed', 'depression', 'down', 'hopeless', 'empty', 'worthless',
    'angry', 'mad', 'furious', 'frustrated', 'rage', 'irritated',
    'lonely', 'alone', 'isolated', 'nobody',
    'sleep', 'insomnia', 'tired', 'exhausted', 'nightmare',
    'relationship', 'breakup', 'broke up', 'left me', 'dumped', 'divorce',
    'trauma', 'ptsd', 'abuse', 'violence', 'hurt',
    'suicide', 'suicidal', 'kill myself', 'self-harm', 'cutting',
    'therapy', 'therapist', 'counseling', 'medication',
    'bipolar', 'schizophrenia', 'ocd', 'adhd', 'eating disorder',
    'grief', 'loss', 'death', 'died', 'mourning',
    'fear', 'phobia', 'scared', 'terrified',
    'overwhelmed', 'burnout', 'pressure',
    'self-esteem', 'confidence', 'insecure',
    'addiction', 'substance', 'alcohol', 'drugs',
    'mental health', 'emotional', 'feeling', 'feelings', 'emotion',
    'cope', 'coping', 'struggling', 'suffering',
    'help', 'support', 'talk', 'listen',
]

# Crisis detection patterns
CRISIS_PATTERNS = [
    r'\b(kill|hurt|harm)\s+(myself|me)\b',
    r'\bsuicid(e|al)\b',
    r'\bend\s+(my|it\s+all)\b',
    r'\bdon\'?t\s+want\s+to\s+live\b',
    r'\bwant\s+to\s+die\b',
    r'\bcut(ting)?\s+(myself|me)\b',
    r'\bno\s+reason\s+to\s+live\b',
    r'\bbetter\s+off\s+dead\b',
    r'\bself[\s-]?harm\b',
]

# Emergency/danger detection patterns (VERY SPECIFIC to avoid false positives)
EMERGENCY_PATTERNS = [
    r'\bsomeone.*following\s+me\b',
    r'\b(gun|knife|weapon).*\b(at|pointed|threatening|has)\b',
    r'\bafraid\b.*\bfollowing\b',
    r'\bin\s+(immediate\s+)?danger\b',
    r'\bstalking\s+me\b',
    r'\battack(ing|ed)\s+me\b',
    r'\bthreaten(ing|ed)\s+(me|my)\b',
    r'\babuse.*happening\b',
]

# Groq API configuration
api_ready = False


def check_api():
    """Check if Groq API key is configured."""
    global api_ready
    
    if GROQ_API_KEY and GROQ_API_KEY != "your_groq_api_key_here":
        logger.info(f"✅ Groq API configured with models:")
        logger.info(f"   Text: {GROQ_MODEL_NAME}")
        logger.info(f"   Vision: {GROQ_VISION_MODEL}")
        api_ready = True
    else:
        logger.warning("Groq API key not configured. Bot will use fallback responses.")
        api_ready = False


def detect_crisis(message: str) -> bool:
    """
    Detect crisis language indicating self-harm or suicidal intent.
    
    Args:
        message: User's message text
        
    Returns:
        True if crisis language detected, False otherwise
    """
    message_lower = message.lower()
    
    for pattern in CRISIS_PATTERNS:
        if re.search(pattern, message_lower, re.IGNORECASE):
            return True
    
    return False


def detect_emergency(message: str) -> bool:
    """
    Detect immediate physical danger or emergency situations.
    
    Args:
        message: User's message text
        
    Returns:
        True if emergency detected, False otherwise
    """
    message_lower = message.lower()
    
    for pattern in EMERGENCY_PATTERNS:
        if re.search(pattern, message_lower, re.IGNORECASE):
            return True
    
    return False


def is_mental_health_related(message: str) -> bool:
    """
    Check if message is related to mental health topics.
    
    Args:
        message: User's message text
        
    Returns:
        True if mental health related, False otherwise
    """
    message_lower = message.lower()
    
    # Check if it's a greeting or short message (allow these)
    greeting_patterns = [
        r'^(hi|hello|hey|good morning|good evening|good afternoon)\b',
        r'^(how are you|what\'?s up|sup)\b',
        r'^(thanks|thank you|ok|okay|yes|no)\b',
    ]
    
    for pattern in greeting_patterns:
        if re.search(pattern, message_lower):
            return True
    
    # If message is very short (< 10 chars), allow it
    if len(message.strip()) < 10:
        return True
    
    # Check for mental health keywords FIRST (allow these)
    for keyword in MENTAL_HEALTH_KEYWORDS:
        if keyword in message_lower:
            return True
    
    # Check for relationship/emotional context indicators (very common in mental health)
    emotional_context = [
        'girl', 'boy', 'guy', 'friend', 'boyfriend', 'girlfriend', 'partner',
        'she', 'he', 'they', 'them', 'her', 'him',
        'fucked', 'messed', 'screwed', 'ruined', 'destroyed',
        'mentioned', 'told', 'said', 'talked',
        'feel', 'feeling', 'felt', 'think', 'thought',
        'problem', 'issue', 'situation', 'thing', 'whole thing',
    ]
    
    for context in emotional_context:
        if context in message_lower:
            return True
    
    # Check for off-topic patterns (reject these) - but only if no emotional context
    for pattern in OFF_TOPIC_PATTERNS:
        if re.search(pattern, message_lower, re.IGNORECASE):
            return False
    
    # If message contains question words but no mental health keywords, it might be off-topic
    question_words = ['what', 'how', 'when', 'where', 'who', 'why', 'which', 'can you', 'tell me', 'calculate', 'solve']
    has_question = any(word in message_lower for word in question_words)
    
    # If it's a specific factual question without emotional context, likely off-topic
    if has_question and len(message.split()) > 5:
        # Check if it's asking for facts/calculations
        factual_indicators = ['capital of', 'what is', 'how many', 'when did', 'where is', 'calculate', 'solve', 'formula']
        if any(indicator in message_lower for indicator in factual_indicators):
            return False
    
    # Default: allow (give benefit of doubt for ambiguous messages)
    return True


def get_off_topic_response() -> str:
    """
    Return polite response for off-topic questions.
    
    Returns:
        Response redirecting to mental health topics
    """
    return (
        "I'm specifically designed to provide mental health and emotional support. "
        "I can't help with that particular topic.\n\n"
        "If you're dealing with stress, anxiety, relationship issues, or any emotional challenges, "
        "I'm here to listen and support you. 💙\n\n"
        "What's on your mind emotionally?"
    )


def get_emergency_response() -> str:
    """Return immediate emergency response."""
    return (
        "🚨 **This sounds like an immediate emergency!**\n\n"
        "**Call emergency services NOW:**\n"
        "• **911** (US) | **112** (EU) | **100** (India) | **999** (UK)\n\n"
        "**If you're in immediate danger:**\n"
        "• Get to a safe, public place\n"
        "• Call police immediately\n"
        "• Stay on the phone with emergency services\n\n"
        "**Your safety is the priority. Get help now!**"
    )


def get_crisis_response() -> str:
    """Return empathetic crisis intervention message."""
    return (
        "🫂 I hear that you're going through an incredibly difficult time right now, "
        "and I'm truly concerned about your safety.\n\n"
        "**Please reach out to someone who can help immediately:**\n\n"
        "🆘 **Emergency Services:** Call 911 (US) or your local emergency number\n"
        "📞 **National Suicide Prevention Lifeline (US):** 988 or 1-800-273-8255\n"
        "💬 **Crisis Text Line:** Text HOME to 741741\n"
        "🌍 **International:** https://findahelpline.com\n\n"
        "You don't have to face this alone. These trained professionals are available "
        "24/7 and truly want to help. Your life has value, and there are people who care."
    )


def get_fallback_response(user_message: str) -> str:
    """
    Return empathetic fallback response when AI is unavailable.
    
    Args:
        user_message: User's message text
        
    Returns:
        Contextual fallback response (3 lines)
    """
    message_lower = user_message.lower()
    
    # Detect emotional keywords for contextual responses
    if any(word in message_lower for word in ['anxious', 'anxiety', 'worried', 'stress', 'nervous']):
        return "I hear that you're feeling anxious.\nThat's a really difficult feeling to carry.\nWhat's weighing on your mind?"
    
    elif any(word in message_lower for word in ['sad', 'depressed', 'down', 'hopeless', 'empty']):
        return "I can sense you're going through a tough time.\nYour feelings are valid and real.\nWhat's been happening?"
    
    elif any(word in message_lower for word in ['angry', 'mad', 'furious', 'frustrated', 'rage', 'fuck', 'pissed', 'hate']):
        return "I hear your anger and frustration.\nThose feelings are completely valid.\nI'm here when you're ready to talk."
    
    elif any(word in message_lower for word in ['lonely', 'alone', 'isolated', 'nobody']):
        return "Feeling alone is one of the hardest things.\nI'm here with you right now.\nYou're not alone in this moment."
    
    elif any(word in message_lower for word in ['focus', 'concentrate', 'study', 'distracted', 'productivity']):
        return "Struggling to focus is really common.\nLet's talk about what's making it hard.\nWhat's going on?"
    
    elif any(word in message_lower for word in ['sleep', 'insomnia', 'tired', 'exhausted', 'can\'t sleep']):
        return "Sleep troubles can affect everything.\nYour exhaustion is real.\nWhat's keeping you up?"
    
    elif any(word in message_lower for word in ['relationship', 'breakup', 'broke up', 'left me', 'dumped']):
        return "Heartbreak is incredibly painful.\nYour feelings are completely valid.\nWant to talk about it?"
    
    elif any(word in message_lower for word in ['money', 'bill', 'debt', 'broke', 'financial', 'afford', 'pay', 'expensive']):
        return "Financial stress is overwhelming.\nThat pressure is real and heavy.\nWhat's happening with your situation?"
    
    elif any(word in message_lower for word in ['work', 'job', 'boss', 'fired', 'unemployed', 'career']):
        return "Work stress can consume everything.\nYour feelings about this are valid.\nWhat's going on at work?"
    
    elif any(word in message_lower for word in ['family', 'parents', 'mom', 'dad', 'sibling']):
        return "Family issues cut deep.\nThose relationships are complicated.\nWhat's happening?"
    
    else:
        return "I'm here to listen and support you.\nYour feelings matter.\nWhat's on your mind?"


async def analyze_image_with_context(image_data: bytes, caption: str, user_id: int) -> str:
    """
    Analyze image with emotional support context using vision model.
    
    Args:
        image_data: Image bytes
        caption: Optional caption from user
        user_id: User ID for context
        
    Returns:
        Empathetic response about the image
    """
    if not api_ready:
        return "I can see you shared an image. While I can't analyze it right now, I'm here to listen. What would you like to tell me about it?"
    
    try:
        # Convert image to base64
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # Build context-aware prompt
        user_context = ""
        if conversation_memory[user_id]:
            recent_msgs = conversation_memory[user_id][-4:]
            user_context = "Recent conversation: " + " ".join([m['content'] for m in recent_msgs if m['role'] == 'user'])
        
        prompt = (
            "You are a mental health support companion analyzing an image someone shared with you. "
            "Provide empathetic, supportive response in 3 short lines (25-35 words). "
            "Acknowledge what you see and connect it to their emotional state. Be warm and understanding. "
            f"{user_context}\n"
            f"User's caption: {caption if caption else 'No caption'}\n"
            "What do you see and how can you support them?"
        )
        
        # Use Groq vision API with proper error handling
        ai_response = None
        
        try:
            # Use Groq vision model (Llama 4 Scout)
            response = requests.post(
                url="https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": GROQ_VISION_MODEL,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_completion_tokens": 150,
                    "temperature": 0.7,
                },
                timeout=15
            )
            
            response.raise_for_status()
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"].strip()
            logger.info(f"✅ Vision response from Groq")
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"Groq vision API HTTP error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
        except Exception as e:
            logger.error(f"Groq vision API error: {e}", exc_info=True)
        
        # If all models failed, use text-only fallback
        if ai_response is None:
            logger.warning("All vision models failed, using text-only response")
            # Generate empathetic response based on caption only
            fallback_response = f"I can see you shared an image with me: '{caption}'. "
            if "left" in caption.lower():
                ai_response = "I hear the pain in your words.\nLosing someone changes us deeply.\nI'm here with you through this."
            elif "sad" in caption.lower() or "hurt" in caption.lower():
                ai_response = "Your pain is real and valid.\nIt's okay to feel what you're feeling.\nI'm here to listen."
            else:
                ai_response = "Thank you for sharing this with me.\nI can sense this means something to you.\nWant to tell me more about it?"
        
        # Store in conversation memory
        conversation_memory[user_id].append({
            "role": "user",
            "content": f"[Shared an image: {caption if caption else 'no caption'}]"
        })
        conversation_memory[user_id].append({
            "role": "assistant",
            "content": ai_response
        })
        
        return ai_response
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API Error analyzing image: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response: {e.response.text}")
        return "I can see you shared something visual with me. What would you like to tell me about it? I'm here to listen."
    except Exception as e:
        logger.error(f"Error analyzing image: {e}", exc_info=True)
        return "I can see you shared something visual with me. What would you like to tell me about it? I'm here to listen."


def generate_ai_response(user_message: str, user_id: int) -> str:
    """
    Generate empathetic AI response using OpenRouter API.
    
    Args:
        user_message: User's message text
        user_id: Telegram user ID for conversation context
        
    Returns:
        AI-generated empathetic response
    """
    if not api_ready:
        return get_fallback_response(user_message)
    
    # Rate limiting per user
    current_time = time.time()
    time_since_last = current_time - last_request_time[user_id]
    
    if time_since_last < MIN_REQUEST_INTERVAL:
        wait_time = MIN_REQUEST_INTERVAL - time_since_last
        time.sleep(wait_time)
    
    last_request_time[user_id] = time.time()
    
    try:
        # Build conversation context
        conversation_memory[user_id].append({
            "role": "user",
            "content": user_message
        })
        
        # Keep only last MAX_MEMORY_LENGTH messages
        if len(conversation_memory[user_id]) > MAX_MEMORY_LENGTH:
            conversation_memory[user_id] = conversation_memory[user_id][-MAX_MEMORY_LENGTH:]
        
        # Full empathetic system prompt with conversation awareness
        system_prompt = (
            "You are a deeply empathetic mental health support companion. Your role is to provide genuine emotional support with warmth and care.\n\n"
            
            "**CRITICAL: SCOPE RESTRICTION**\n"
            "You ONLY provide support for mental health, emotional wellbeing, and psychological topics including:\n"
            "- Anxiety, depression, stress, trauma, grief\n"
            "- Relationship issues, breakups, loneliness\n"
            "- Self-esteem, confidence, identity\n"
            "- Sleep issues, burnout, overwhelm\n"
            "- Anger, fear, emotional regulation\n"
            "- Life transitions, loss, coping strategies\n\n"
            
            "**CRITICAL: If asked about unrelated topics (riddles, puzzles, car colors, weather, sports, cooking, math, coding, news, etc.):**\n"
            "- DO NOT answer the question at all\n"
            "- DO NOT 'play along' or engage with the off-topic content\n"
            "- Politely decline and immediately redirect to mental health support\n"
            "- Keep it brief and redirect\n\n"
            
            "RESPONSE STYLE:\n"
            "- Be warm, caring, and deeply empathetic\n"
            "- Validate their pain without minimizing it\n"
            "- Show you truly understand their suffering\n"
            "- Offer comfort, hope, and perspective\n"
            "- Be SPECIFIC to their exact situation\n"
            "- Remember conversation context and build on it\n"
            "- DO NOT repeat or paraphrase what they said - jump straight to empathy and support\n"
            "- Start with validation, not summary\n\n"
            
            "RESPONSE LENGTH:\n"
            "- ALWAYS use exactly 3 lines (35-50 words total)\n"
            "- Keep each line concise and impactful\n"
            "- No more than 3 lines, even for deep pain\n"
            "- Make every word count\n\n"
            
            "WHAT TO DO:\n"
            "✓ Acknowledge their specific pain (heartbreak, loss, violence thoughts, etc)\n"
            "✓ Validate that their feelings make sense\n"
            "✓ Offer gentle perspective and hope\n"
            "✓ Show you care about them as a person\n"
            "✓ Suggest concrete next steps when appropriate (therapy, helplines, etc)\n\n"
            
            "WHAT NOT TO DO:\n"
            "✗ NEVER ask questions at the end (no 'What happened?', 'Want to talk?', 'How are you feeling?')\n"
            "✗ Don't repeat or explain what they said\n"
            "✗ Don't give generic 'everything will be okay' platitudes\n"
            "✗ Don't minimize their pain\n"
            "✗ Don't be robotic or detached\n"
            "✗ Don't answer questions outside mental health scope\n"
            "✗ Don't exceed 3 lines\n\n"
            
            "EXAMPLES (EXACTLY 3 LINES, NO QUESTIONS):\n"
            
            "User: 'm feeling lonely bcz of her'\n"
            "Good: 'That ache of missing someone who meant everything is unbearable. The emptiness she left behind feels impossible to fill. You're grieving a profound loss, and that takes time.'\n"
            "Bad: 'Your heart is aching from the absence of this person, and the loneliness is overwhelming. [REPEATING] Would you like to talk more? [ASKING QUESTION]'\n\n"
            
            "User: 'she was my world'\n"
            "Good: 'Losing someone who was your entire world shatters everything. That kind of love doesn't just disappear, and neither does the pain. You're allowed to grieve this deeply.'\n"
            "Bad: 'Losing her feels like losing a part of yourself. She was your everything... [TOO LONG, EXPLAINING WHAT THEY SAID]'\n\n"
            
            "User: 'U know the girl I mentioned she really fucked up whole thing'\n"
            "Good: 'That betrayal cuts so deep. When someone destroys what you built together, the anger and hurt are overwhelming. You deserved better than this.'\n"
            "Bad: 'It's clear that this girl's actions have caused you pain. [REPEATING] What happened? [ASKING QUESTION]'\n\n"
            
            "User: 'I bought a red car. Then I said it was blue. What color is my car?'\n"
            "Good: 'I'm here for mental health and emotional support, not riddles. If you're dealing with stress or emotional challenges, I'm here for you. 💙'\n"
            "Bad: 'I'll play along - your car is red. [ANSWERING OFF-TOPIC]'\n\n"
            
            "User: 'Shall I kill her'\n"
            "Good: 'That rage is consuming you, but acting on it would destroy your life too. You need immediate support to process this safely. Please call 911 or 988 crisis line right now.'\n"
            "Bad: 'I hear your pain. The anger is intense. But don't act on it. Call for help. [TOO CHOPPY, 4 LINES]'\n\n"
            
            "For crisis/self-harm: Urge emergency services (911/988/112/100) with empathy.\n"
            "For violence thoughts: Acknowledge pain, urge crisis support, emphasize their worth."
        )
        
        # Build messages for API with full conversation context
        messages = [{"role": "system", "content": system_prompt}]
        # Use last 10 messages (5 exchanges) for better context
        messages.extend(conversation_memory[user_id][-10:])
        
        # Call Groq API
        try:
            response = requests.post(
                url="https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": GROQ_MODEL_NAME,
                    "messages": messages,
                    "temperature": 0.85,
                    "max_tokens": 80,  # Strict limit for concise 3-line responses
                    "top_p": 0.95,
                },
                timeout=10
            )
            
            response.raise_for_status()
            result = response.json()
            
        except Exception as e:
            logger.error(f"Groq API error: {e}, using fallback response")
            return get_fallback_response(user_message)
        
        ai_response = result["choices"][0]["message"]["content"].strip()
        
        # Store assistant response in memory
        conversation_memory[user_id].append({
            "role": "assistant",
            "content": ai_response
        })
        
        return ai_response
        
    except requests.exceptions.RequestException as e:
        logger.error(f"OpenRouter API error: {e}")
        return get_fallback_response(user_message)
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        return get_fallback_response(user_message)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    welcome_message = (
        "🌟 **Welcome to Your Mental Health Support Companion** 🌟\n\n"
        "I'm here to listen and provide emotional support whenever you need it. "
        "This is a safe, judgment-free space where you can share what's on your mind.\n\n"
        "**Important Disclaimer:**\n"
        "• I provide emotional support, not medical or professional advice\n"
        "• I'm not a replacement for licensed mental health professionals\n"
        "• In crisis situations, please contact emergency services immediately\n\n"
        "**Available Commands:**\n"
        "/help - Show available commands\n"
        "/resources - Crisis helplines and mental health resources\n\n"
        "💙 Feel free to share what's on your mind. I'm here to listen."
    )
    
    await update.message.reply_text(welcome_message, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_message = (
        "**Available Commands:**\n\n"
        "/start - Welcome message and introduction\n"
        "/help - Show this help message\n"
        "/resources - Crisis helplines and mental health resources\n\n"
        "**How to Use:**\n"
        "Simply send me a message about what's on your mind, and I'll respond with "
        "empathetic support. I remember our recent conversation to provide better context.\n\n"
        "**Privacy:**\n"
        "Your messages are processed in memory only and not permanently stored. "
        "Your privacy and safety are my top priorities."
    )
    
    await update.message.reply_text(help_message, parse_mode='Markdown')


async def resources_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /resources command."""
    resources_message = (
        "🆘 **Crisis Helplines & Mental Health Resources**\n\n"
        "**Immediate Crisis Support:**\n"
        "• **988 Suicide & Crisis Lifeline (US):** Call/Text 988\n"
        "• **National Suicide Prevention Lifeline:** 1-800-273-8255\n"
        "• **Crisis Text Line:** Text HOME to 741741\n"
        "• **Emergency Services:** 911 (US) or local emergency number\n\n"
        "**International Resources:**\n"
        "• **Find A Helpline:** https://findahelpline.com\n"
        "• **Befrienders Worldwide:** https://befrienders.org\n\n"
        "**Mental Health Support:**\n"
        "• **NAMI Helpline:** 1-800-950-6264 (Mon-Fri, 10am-10pm ET)\n"
        "• **SAMHSA National Helpline:** 1-800-662-4357 (24/7)\n"
        "• **Therapy Resources:** https://psychologytoday.com\n\n"
        "**Online Communities:**\n"
        "• **7 Cups:** https://7cups.com (free emotional support)\n"
        "• **r/SuicideWatch:** Reddit support community\n\n"
        "💙 Remember: Reaching out for help is a sign of strength, not weakness."
    )
    
    await update.message.reply_text(resources_message, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle incoming user messages with crisis detection and AI response.
    Buffers rapid messages to avoid multiple responses.
    """
    user_message = update.message.text
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name
    
    # Try to get phone number from Telegram user data (if shared)
    user_phone = None
    try:
        # Get full user info
        chat_member = await context.bot.get_chat(user_id)
        if hasattr(chat_member, 'phone_number'):
            user_phone = chat_member.phone_number
    except:
        # If not available, try from update
        if hasattr(update.effective_user, 'phone_number'):
            user_phone = update.effective_user.phone_number
    
    current_time = time.time()
    
    # Add message to buffer
    user_message_buffer[user_id].append(user_message)
    last_message_time[user_id] = current_time
    
    # Wait to see if more messages are coming
    import asyncio
    await asyncio.sleep(MESSAGE_WAIT_TIME)
    
    # Check if this is still the last message
    if current_time != last_message_time[user_id]:
        # Newer message came in, let that one handle the response
        return
    
    # Combine all buffered messages
    if not user_message_buffer[user_id]:
        return
    
    user_message = " ".join(user_message_buffer[user_id])
    user_message_buffer[user_id] = []  # Clear buffer
    
    logger.info(f"Processing combined message from {username} (ID: {user_id}): {user_message[:50]}...")
    
    # Check if message is mental health related (topic validation)
    if not is_mental_health_related(user_message):
        logger.info(f"Off-topic message detected from user {user_id}")
        await update.message.reply_text(get_off_topic_response())
        return
    
    # Emergency detection (physical danger) - highest priority
    if detect_emergency(user_message):
        logger.error(f"EMERGENCY DETECTED from user {user_id}")
        
        # Send emergency response
        await update.message.reply_text(get_emergency_response(), parse_mode='Markdown')
        
        # Notify admin if configured
        if ADMIN_CHAT_ID:
            try:
                admin_alert = (
                    f"🚨 **EMERGENCY ALERT**\n\n"
                    f"User: {username} (ID: {user_id})\n"
                    f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Message: {user_message[:200]}"
                )
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=admin_alert,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Failed to send admin alert: {e}")
        
        return
    
    # Crisis detection (self-harm/suicide)
    if detect_crisis(user_message):
        logger.warning(f"CRISIS DETECTED from user {user_id}")
        
        # Send crisis response
        await update.message.reply_text(get_crisis_response(), parse_mode='Markdown')
        
        # Notify admin if configured
        if ADMIN_CHAT_ID:
            try:
                admin_alert = (
                    f"⚠️ **CRISIS ALERT**\n\n"
                    f"User: {username} (ID: {user_id})\n"
                    f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Message: {user_message[:200]}"
                )
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=admin_alert,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Failed to send admin alert: {e}")
        
        return
    
    # Show typing indicator
    await update.message.chat.send_action(action="typing")
    
    # Generate AI response
    response = generate_ai_response(user_message, user_id)
    
    # Get phone number: first try from Telegram profile, then extract from message
    phone_number = user_phone or extract_phone_number(user_message)
    
    # Save to Google Sheets (username, phone, question, answer)
    if sheets_enabled and save_to_sheets:
        try:
            save_to_sheets(username, phone_number, user_message, response)
        except Exception as e:
            logger.error(f"Failed to save to Google Sheets: {e}")
    
    # Send response
    await update.message.reply_text(response)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle photo messages with emotional support context.
    """
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name
    
    # Try to get phone number from Telegram user data
    user_phone = None
    try:
        chat_member = await context.bot.get_chat(user_id)
        if hasattr(chat_member, 'phone_number'):
            user_phone = chat_member.phone_number
    except:
        if hasattr(update.effective_user, 'phone_number'):
            user_phone = update.effective_user.phone_number
    
    caption = update.message.caption or ""
    
    logger.info(f"Photo from {username} (ID: {user_id}) with caption: {caption[:50] if caption else 'none'}...")
    
    # Show typing indicator
    await update.message.reply_chat_action("typing")
    
    try:
        # Get the largest photo
        photo = update.message.photo[-1]
        photo_file = await photo.get_file()
        
        # Download photo as bytes
        photo_bytes = await photo_file.download_as_bytearray()
        
        # Analyze image with context
        response = await analyze_image_with_context(bytes(photo_bytes), caption, user_id)
        
        # Get phone number: first try from Telegram profile, then extract from caption
        phone_number = user_phone or (extract_phone_number(caption) if caption else None)
        
        # Save to Google Sheets (username, phone, question, answer)
        if sheets_enabled and save_to_sheets:
            try:
                user_msg = f"[Image] {caption}" if caption else "[Image sent]"
                save_to_sheets(username, phone_number, user_msg, response)
            except Exception as e:
                logger.error(f"Failed to save to Google Sheets: {e}")
        
        # Send response
        await update.message.reply_text(response)
        
    except Exception as e:
        logger.error(f"Error handling photo: {e}")
        await update.message.reply_text(
            "I can see you shared an image with me. "
            "What would you like to tell me about it? I'm here to listen."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors in the bot."""
    logger.error(f"Update {update} caused error {context.error}")


def main():
    """Start the bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
        return
    
    logger.info("Starting Mental Health Support Bot...")
    
    # Check API configuration
    check_api()
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("resources", resources_command))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))  # Photo handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    # Start bot
    logger.info("Bot is running! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


def create_web_app():
    """Create Flask app to serve the website"""
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    website_dir = os.path.join(base_dir, 'website')
    
    app = Flask(__name__, static_folder=website_dir, static_url_path='')
    
    @app.route('/')
    def index():
        return send_from_directory(website_dir, 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(website_dir, path)
    
    return app


def run_web_server():
    """Run Flask web server in a separate thread"""
    app = create_web_app()
    port = int(os.getenv('PORT', 8080))
    logger.info(f"🌐 Starting web server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    # Start web server in background thread
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    logger.info("✅ Web server started in background")
    
    # Start Telegram bot (main thread)
    main()
