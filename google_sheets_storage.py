#!/usr/bin/env python3
"""
Simple Google Sheets storage for MiraiBot conversations
Stores: Username, User Question, Bot Answer
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
import os

logger = logging.getLogger(__name__)

# Your Google Sheet ID
SHEET_ID = '1hardTfwdlSpk55wpDoXIL1HwEQdJXh6N4QcXl9rgNzM'

class GoogleSheetsStorage:
    """Simple Google Sheets storage"""
    
    def __init__(self):
        self.sheet = None
        self.enabled = False
        
        try:
            # Check for credentials
            if not os.path.exists('google_credentials.json'):
                logger.warning("⚠️ google_credentials.json not found - Google Sheets storage disabled")
                return
            
            # Setup credentials
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            creds = ServiceAccountCredentials.from_json_keyfile_name('google_credentials.json', scope)
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
