#!/bin/bash
# Stop all Telegram Bot instances

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

# Verify all stopped
if pgrep -f telegram_bot.py > /dev/null; then
    echo "❌ Some instances may still be running"
    echo "Running processes:"
    ps aux | grep telegram_bot.py | grep -v grep
else
    echo "✅ All bot instances stopped successfully"
fi
