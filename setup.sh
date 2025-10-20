#!/bin/bash
# Quick setup script for Mental Health Support Bot

set -e

echo "🧠 Mental Health Support Bot - Quick Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "Error: Python 3 not found!"; exit 1; }

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your tokens!"
    echo "   - TELEGRAM_BOT_TOKEN (from @BotFather)"
    echo "   - HF_TOKEN (from huggingface.co)"
    echo ""
    echo "Run: nano .env"
else
    echo ".env file already exists, skipping..."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file: nano .env"
echo "2. Add your TELEGRAM_BOT_TOKEN and HF_TOKEN"
echo "3. Run the bot: python telegram_bot.py"
echo ""
echo "For deployment options, see DEPLOYMENT.md"
