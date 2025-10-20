#!/bin/bash
# Restart Telegram Bot Script

echo "🛑 Stopping all bot instances..."

# Kill all python processes running telegram_bot.py
pkill -f telegram_bot.py

# Wait a moment
sleep 2

# Check if any instances are still running
if pgrep -f telegram_bot.py > /dev/null; then
    echo "⚠️  Force killing remaining instances..."
    pkill -9 -f telegram_bot.py
    sleep 1
fi

echo "✅ All bot instances stopped"
echo ""
echo "🚀 Starting bot..."
echo ""

# Start the bot
python3 telegram_bot.py
