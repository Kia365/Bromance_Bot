# LangChain agent logic for bromance-bot

from telegram_search import search_groups_and_scrape_users
from llm_utils import call_llm

def run_bromance_agent():
    print("Welcome to Bromance Bot!")
    interests = input("What are your interests? (comma separated): ")
    print("Searching Telegram for people who share your interests...")
    # Search Telegram for groups/channels and scrape user data
    user_profiles = search_groups_and_scrape_users(interests)
    if not user_profiles:
        print("Sorry, couldn't find any relevant users.")
        return
    # Use LLM to select 5 usernames
    prompt = f"""
You are an expert at making friends. Given the following user profiles, select 5 usernames that best match the interest(s): {interests}.

User profiles:
{user_profiles}

Return only the 5 usernames, comma separated.
"""
    try:
        usernames = call_llm(prompt)
        print("Here are 5 people you might want to talk to:")
        print(usernames)
    except Exception as e:
        print(f"Error calling LLM: {e}") 