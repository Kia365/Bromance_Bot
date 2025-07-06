import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler
from telegram_search import search_groups_and_scrape_users
from llm_utils import call_llm

load_dotenv()

BOT_TOKEN = os.getenv("BROMANCE_BOT_TOKEN")
ASK_INTERESTS = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I'm Bromance Bot. Tell me your interests (comma separated), and I'll find people you might want to talk to!"
    )
    return ASK_INTERESTS

async def handle_interests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    interests = update.message.text
    await update.message.reply_text("Searching Telegram for people who share your interests...")
    user_profiles = search_groups_and_scrape_users(interests)
    if not user_profiles:
        await update.message.reply_text("Sorry, couldn't find any relevant users.")
        return ConversationHandler.END
    prompt = f"""
You are an expert at making friends. Given the following user profiles, select 5 usernames that best match the interest(s): {interests}.

User profiles:
{user_profiles}

Return only the 5 usernames, comma separated.
"""
    usernames = call_llm(prompt)
    await update.message.reply_text(f"Here are 5 people you might want to talk to:\n{usernames}")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bye! If you want to try again, just type /start.")
    return ConversationHandler.END

def main():
    if not BOT_TOKEN:
        print("BROMANCE_BOT_TOKEN not set in .env file!")
        return
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASK_INTERESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_interests)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    app.add_handler(conv_handler)
    print("Bromance Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main() 