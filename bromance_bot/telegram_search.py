# Telethon logic for searching Telegram groups and users

from telethon import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_NAME = "bromance_bot_session"

# Helper to get or create a Telegram client

def get_telegram_client():
    if not API_ID or not API_HASH:
        raise ValueError("TELEGRAM_API_ID and TELEGRAM_API_HASH must be set in .env file!")
    return TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def async_search_groups_and_scrape_users(interests: str):
    client = get_telegram_client()
    await client.start()
    # Search for public groups/channels by interest keywords
    interests_list = [i.strip() for i in interests.split(",") if i.strip()]
    found_users = []
    for interest in interests_list:
        async for dialog in client.iter_dialogs():
            if dialog.is_group or dialog.is_channel:
                if interest.lower() in dialog.name.lower():
                    # Scrape members (limited to first 50 for demo)
                    async for user in client.iter_participants(dialog.id, limit=50):
                        if user.username:
                            found_users.append({
                                "username": user.username,
                                "bio": user.about if hasattr(user, 'about') else "",
                                "interests": [interest],
                            })
    await client.disconnect()
    return found_users

def search_groups_and_scrape_users(interests: str):
    import asyncio
    try:
        return asyncio.run(async_search_groups_and_scrape_users(interests))
    except Exception as e:
        print(f"Error searching Telegram: {e}")
        return []

# TODO: Implement functions to search groups/channels and scrape user data 