import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Activăm logging-ul pentru debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Obținem token-ul botului din variabilele de mediu
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: CallbackContext) -> None:
    """Comanda /start"""
    await update.message.reply_text("Hello! I'm AbioAIBot 🤖. How can I assist you today?")

async def help_command(update: Update, context: CallbackContext) -> None:
    """Comanda /help"""
    await update.message.reply_text("Use /recommend [category] to get AI product recommendations!")

async def recommend(update: Update, context: CallbackContext) -> None:
    """Comanda /recommend pentru recomandări de produse AI"""
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please specify a category, e.g. /recommend image-tools")
        return
    await update.message.reply_text(f"Here are some AI tools for {query}:\n1. Tool AI 1\n2. Tool AI 2\n3. Tool AI 3")

async def echo(update: Update, context: CallbackContext) -> None:
    """Repetă mesajele utilizatorilor pentru test"""
    await update.message.reply_text(update.message.text)

# Configurăm botul
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("recommend", recommend))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Pornim botul
if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()

# Fișier requirements.txt
REQUIREMENTS_TXT = """
python-telegram-bot==20.0
"""

# Fișier Procfile pentru Railway
PROCFILE = """
worker: python bot.py
"""

# Fișier README.md
README_MD = """
# AbioAIBot 🤖
A Telegram bot that provides AI product recommendations.

## How to use:
- `/start` - Start the bot
- `/help` - Get usage instructions
- `/recommend [category]` - Get AI product recommendations

## Deployment
Hosted on Railway.app for continuous operation.
"""
