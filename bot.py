import os
import logging
import random
import requests
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import CommandHandler, MessageHandler, filters, Dispatcher, CallbackContext
import openai

# Logging qurulması
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(_name_)

# Ərtaf mühit dəyişənləri
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    logger.error("TELEGRAM_TOKEN təyin edilməyib!")
    exit(1)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

ADMIN_IDS = list(map(int, os.environ.get("ADMIN_IDS", "").split(',')))

# Bot instansiyası
bot = Bot(token=TOKEN)

# Flask tətbiqi
app = Flask(_name_)

# Dispatcher yaradılır
dispatcher = Dispatcher(bot, None, workers=0)

# Funksiya: /reverse
def reverse(update: Update, context: CallbackContext):
    text = " ".join(context.args)
    update.message.reply_text(text[::-1])

# Funksiya: /8ball
def eightball(update: Update, context: CallbackContext):
    responses = ["Bəli", "Xeyr", "Bilmərəm", "Şans var"]
    update.message.reply_text(random.choice(responses))

# Funksiya: /meme
def meme(update: Update, context: CallbackContext):
    meme_url = "https://api.memegen.link/images/buzz/meme/time.png"
    update.message.reply_photo(meme_url)

# Funksiya: /translate
def translate(update: Update, context: CallbackContext):
    update.message.reply_text("Tərcümə funksiyası hələ dəyişdirilir.")

# Funksiya: /weather
def weather(update: Update, context: CallbackContext):
    update.message.reply_text("Hava proqnozu funksiyası hələ dəyişdirilir.")

# Funksiya: /roast
def roast(update: Update, context: CallbackContext):
    insults = ["Sənə səhv düymə basmısan", "Gülməli deyildi", "Yaxşı düşün"]
    update.message.reply_text(random.choice(insults))

# Funksiya: /fortune
def fortune(update: Update, context: CallbackContext):
    fortunes = ["Bu gün uğur səni tapacaq", "Daha çox şans lazımdır"]
    update.message.reply_text(random.choice(fortunes))

# Funksiya: /fact
def fact(update: Update, context: CallbackContext):
    facts = ["Dünya yuvarlaq deyil", "Su islanmır"]
    update.message.reply_text(random.choice(facts))

# Funksiya: /ascii
def ascii_art(update: Update, context: CallbackContext):
    update.message.reply_text("ASCII funksiya hələ dəyişdirilir.")

# Funksiya: /stickerify
def stickerify(update: Update, context: CallbackContext):
    update.message.reply_text("Sticker funksiyası hələ dəyişdirilir.")

# Funksiya: /bilgi
def bilgi(update: Update, context: CallbackContext):
    info_text = (
        "Meri Bot \n"
        "\n"
        "\u2022 /reverse - Mətni tərs çevirir \n"
        "\u2022 /8ball - Sehrli top cavab verir \n"
        "\u2022 /meme - Təsadüfi meme göndərir \n"
        "\u2022 /translate - Mətni tərcümə edir \n"
        "\u2022 /weather - Hava proqnozu \n"
        "\u2022 /roast - Sataşma \n"
        "\u2022 /fortune - Bəxt proqnozu \n"
        "\u2022 /fact - Maraqlı fakt \n"
        "\u2022 /ascii - ASCII sənəti \n"
        "\u2022 /stickerify - Sticker düzəldir \n"
        "\n"
        "Botun Yazıçısı: Şirvan Əliyev \n"
        "Botun Developer'i: Məryəm Əliyeva"
    )
    update.message.reply_text(info_text)

# Handlerlər
dispatcher.add_handler(CommandHandler("reverse", reverse))
dispatcher.add_handler(CommandHandler("8ball", eightball))
dispatcher.add_handler(CommandHandler("meme", meme))
dispatcher.add_handler(CommandHandler("translate", translate))
dispatcher.add_handler(CommandHandler("weather", weather))
dispatcher.add_handler(CommandHandler("roast", roast))
dispatcher.add_handler(CommandHandler("fortune", fortune))
dispatcher.add_handler(CommandHandler("fact", fact))
dispatcher.add_handler(CommandHandler("ascii", ascii_art))
dispatcher.add_handler(CommandHandler("stickerify", stickerify))
dispatcher.add_handler(CommandHandler("bilgi", bilgi))

# Webhook üçün endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

# Əsas səhifə
@app.route("/")
def index():
    return "Meri bot işləyir."

if _name_ == "_main_":
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
    if WEBHOOK_URL:
        bot.set_webhook(WEBHOOK_URL + "/webhook")
        logger.info(f"Webhook quruldu: {WEBHOOK_URL}/webhook")
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
