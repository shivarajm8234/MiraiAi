#!/usr/bin/env python3
"""
Simple Google Sheets storage for MiraiBot conversations
Stores: Username, User Question, Bot Answer
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
import os
import base64
import json
import tempfile

logger = logging.getLogger(__name__)

# Your Google Sheet ID
SHEET_ID = '1hardTfwdlSpk55wpDoXIL1HwEQdJXh6N4QcXl9rgNzM'

def get_credentials_file():
    """
    Get credentials file path - works for both local and deployment
    
    Returns:
        str: Path to credentials file, or None if not found
    """
    # Option 1: Local file (for development)
    if os.path.exists('google_credentials.json'):
        logger.info("📁 Using local google_credentials.json")
        return 'google_credentials.json'
    
    # Option 2: Environment variable (for deployment)
    base64_creds = os.getenv('GOOGLE_CREDENTIALS_BASE64')
    if base64_creds:
        try:
            logger.info("🔐 Using GOOGLE_CREDENTIALS_BASE64 from environment")
            # Decode base64
            creds_json = base64.b64decode(base64_creds).decode('utf-8')
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
            temp_file.write(creds_json)
            temp_file.close()
            
            logger.info(f"✅ Created temporary credentials file: {temp_file.name}")
            return temp_file.name
        except Exception as e:
            logger.error(f"❌ Failed to decode credentials from environment: {e}")
            return None
    
    logger.warning("⚠️ No credentials found (neither file nor environment variable)")
    return None

class GoogleSheetsStorage:
    """Simple Google Sheets storage"""
    
    def __init__(self):
        self.sheet = None
        self.enabled = False
        self.temp_creds_file = None
        
        try:
            # Get credentials file (local or from environment)
            creds_file = get_credentials_file()
            if not creds_file:
                logger.warning("⚠️ Google Sheets storage disabled - no credentials found")
                return
            
            self.temp_creds_file = creds_file if creds_file != 'google_credentials.json' else None
            
            # Setup credentials
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
            client = gspread.authorize(creds)
            
            # Open your specific sheet
            self.sheet = client.open_by_key(SHEET_ID).sheet1
            self.enabled = True
            logger.info(f"✅ Connected to Google Sheet: {SHEET_ID}")
            
            # Add headers if sheet is empty
            if self.sheet.row_count == 0 or not self.sheet.cell(1, 1).value:
                self.sheet.append_row(["Username", "User Question", "Bot Answer"])
                logger.info("📋 Added headers to sheet")
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to Google Sheets: {e}")
            logger.error("Make sure the sheet is shared with your service account email")
        finally:
            # Clean up temporary file if created
            if self.temp_creds_file and os.path.exists(self.temp_creds_file):
                try:
                    os.unlink(self.temp_creds_file)
                except:
                    pass
    
    def save_conversation(self, username: str, question: str, answer: str):
        """
        Save conversation to Google Sheets
        
        Args:
            username: Telegram username
            question: User's question
            answer: Bot's answer
        """
        if not self.enabled:
            return False
        
        try:
            # Prepare row with only 3 columns
            row = [
                username or "Unknown",
                question[:500],  # Limit length
                answer[:1000]    # Limit length
            ]
            
            # Append to sheet
            self.sheet.append_row(row, value_input_option='USER_ENTERED')
            logger.info(f"💾 Saved to Google Sheets: {username}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to save to Google Sheets: {e}")
            return False

# Global instance
sheets_storage = None

def init_sheets_storage():
    """Initialize global storage"""
    global sheets_storage
    sheets_storage = GoogleSheetsStorage()
    return sheets_storage

def save_conversation(username: str, question: str, answer: str):
    """Save conversation to sheets"""
    if sheets_storage and sheets_storage.enabled:
        return sheets_storage.save_conversation(username, question, answer)
    return False
