# API Keys Configuration

## Groq API Keys (3 Total)

The bot uses **3 Groq API keys** with automatic failover:

### Primary Key
- Environment variable: `GROQ_API_KEY`
- Used first for all requests

### Backup Keys
1. **Backup Key 1**: Environment variable `GROQ_API_KEY_1`
2. **Backup Key 2**: Environment variable `GROQ_API_KEY_2`

> **Note**: All keys are stored as environment variables for security. Set them in your `.env` file locally or in Railway's Variables tab for deployment.

## How Automatic Failover Works

1. **Normal Operation**: Bot uses primary key from `.env`
2. **Rate Limit Hit (429 error)**: Bot automatically switches to Backup Key 1
3. **Backup 1 Rate Limited**: Bot switches to Backup Key 2
4. **All Keys Limited**: Bot shows error message to user

## Rate Limits (Groq Free Tier)

- **100,000 tokens per day** per API key
- With 3 keys: **300,000 tokens per day total**
- Automatic rotation ensures continuous service

## Monitoring

Check logs for:
- `✅ Groq API configured with 3 API key(s)` - All keys loaded
- `🔄 Switched to backup API key #2` - Failover occurred
- `✅ Successfully used backup API key` - Backup working

## Security Note

⚠️ **Backup keys are hardcoded in `telegram_bot.py`**
- This is intentional for automatic failover
- Keys are in a private repository
- When deploying to Railway, keys are included in the code
- For production, consider using environment variables for all keys

## Upgrading

To increase limits:
1. Upgrade Groq tier at: https://console.groq.com/settings/billing
2. Or add more backup keys to `GROQ_API_KEYS` array in `telegram_bot.py`
