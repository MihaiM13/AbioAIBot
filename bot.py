import logging
import os
import json
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Configurare logging pentru debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)

# Setăm permisiunile pentru API
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Obținem credențialele Google din variabila de mediu
CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS")

if not CREDENTIALS_JSON:
    logging.error("Eroare: Variabila GOOGLE_CREDENTIALS nu este setată!")
    exit(1)

try:
    creds_dict = json.loads(CREDENTIALS_JSON)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
    client = gspread.authorize(creds)
    logging.info("Autentificare Google Sheets reușită!")
except Exception as e:
    logging.error(f"Eroare la autentificarea cu Google Sheets: {e}")
    exit(1)

# Deschidem Google Sheets
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

try:
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    sheet = spreadsheet.sheet1
    logging.info("Conectare la Google Sheets reușită!")
except Exception as e:
    logging.error(f"Eroare la conectarea Google Sheets: {e}")
    exit(1)

# Funcție pentru a scrie în Google Sheets

def adauga_date_in_sheets(update: Update, text):
    """Salvează în Google Sheets numele utilizatorului, ID-ul, mesajul și timestamp-ul."""
    user = update.message.from_user
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    date = [user.full_name, user.id, text, timestamp]
    
    try:
        sheet.append_row(date)
        logging.info(f"Datele {date} au fost adăugate cu succes în Google Sheets!")
    except Exception as e:
        logging.error(f"Eroare la scrierea în Google Sheets: {e}")

# Obținem token-ul botului din variabilele de mediu
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    logging.error("Eroare: Variabila de mediu TELEGRAM_BOT_TOKEN nu este setată!")
    exit(1)

# Restul codului pentru Telegram Bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! I'm AbioAIBot 🤖. How can I assist you today?")

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Use /recommend [category] to get AI product recommendations!")

async def save_data(update: Update, context: CallbackContext) -> None:
    text = " ".join(context.args)

    if not text:
        await update.message.reply_text("Te rog introdu textul pe care vrei să-l salvezi.")
        return

    adauga_date_in_sheets(update, text)
    await update.message.reply_text(f"Textul '{text}' a fost salvat în Google Sheets!")

async def recommend(update: Update, context: CallbackContext) -> None:
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please specify a category, e.g. /recommend image-tools")
        return
    await update.message.reply_text(f"Here are some AI tools for {query}:
1. Tool AI 1
2. Tool AI 2
3. Tool AI 3")

async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

# Configurăm botul
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("recommend", recommend))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.add_handler(CommandHandler("save", save_data))

# Pornim botul
if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
