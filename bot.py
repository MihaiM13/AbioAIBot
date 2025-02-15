import logging
import os
import gspread
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

# Setăm calea corectă pentru credențiale (asigură-te că fișierul este în același folder cu acest script)
CREDENTIALS_FILE = "abioaibot-api-0226e1c30d25.json"

# Verificare existența fișierului JSON înainte de utilizare
if not os.path.exists(CREDENTIALS_FILE):
    logging.error(f"Eroare: Fișierul {CREDENTIALS_FILE} nu există! Verifică numele și locația fișierului.")
    exit(1)

# Autorizare Google Sheets
try:
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
    client = gspread.authorize(creds)
    logging.info("Autorizare Google Sheets reușită!")
except Exception as e:
    logging.error(f"Eroare la autentificarea Google Sheets: {e}")
    exit(1)

# Deschidem Google Sheets (înlocuiește cu ID-ul corect al documentului tău)
SPREADSHEET_ID = "1hdHFipVgP16JAFgGffRD0R7zWaVzOPQkEvSAGTjhhjc"

try:
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    sheet = spreadsheet.sheet1
    logging.info("Conectare la Google Sheets reușită!")
except Exception as e:
    logging.error(f"Eroare la conectarea Google Sheets: {e}")
    exit(1)

# Funcție pentru a scrie în Google Sheets
def adauga_date_in_sheets(date):
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


# Restul codului...

async def start(update: Update, context: CallbackContext) -> None:
    """Comanda /start"""
    await update.message.reply_text("Hello! I'm AbioAIBot 🤖. How can I assist you today?")

async def help_command(update: Update, context: CallbackContext) -> None:
    """Comanda /help"""
    await update.message.reply_text("Use /recommend [category] to get AI product recommendations!")

async def save_data(update: Update, context: CallbackContext) -> None:
    """Comanda /save pentru a salva date în Google Sheets"""
    text = " ".join(context.args)

    # Debugging
    print(f"Comanda /save a fost apelată cu textul: {text}")
    await update.message.reply_text(f"Primit text: {text}")

    if not text:
        await update.message.reply_text("Te rog introdu textul pe care vrei să-l salvezi.")
        return

    adauga_date_in_sheets([text])  # Adăugăm textul într-un rând nou

    await update.message.reply_text(f"Textul '{text}' a fost salvat în Google Sheets!")


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
app.add_handler(CommandHandler("save", save_data))

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
