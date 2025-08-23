# Initial Setup Instructions

## Prerequisites
- Python 3.11+ installed
- Git installed

## Step-by-Step Setup

### 1. Clone and Navigate
```bash
git clone <your-repo-url>
cd deadline-reminder-bot
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install notion-client discord.py python-dotenv
```

### 4. Set Up Environment Variables
```bash
mkdir -p env-vars
cp .env.example env-vars/.env
```

Edit `env-vars/.env` with your actual tokens:
```
NOTION_TOKEN=your_notion_token_here
NOTION_DATABASE_ID=your_database_id_here
DISCORD_TOKEN=your_discord_token_here
DISCORD_CHANNEL_ID=your_channel_id_here
```

### 5. Get API Tokens

**Notion Integration:**
1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Create new integration
3. Copy the token to `NOTION_TOKEN`
4. Share your database with the integration
5. Copy database ID from URL to `NOTION_DATABASE_ID`

**Discord Bot:**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create new application
3. Go to Bot section, create bot
4. Copy token to `DISCORD_TOKEN`
5. Get channel ID (right-click channel → Copy ID) to `DISCORD_CHANNEL_ID`

### 6. Test the Bot
```bash
source venv/bin/activate && python bot.py
```

## Daily Usage
Always activate virtual environment before running:
```bash
source venv/bin/activate
python bot.py
```