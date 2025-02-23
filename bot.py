import os
import telebot
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# Function to fetch horoscope data
def get_daily_horoscope(sign: str, day: str) -> dict:
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)
    return response.json()

# Start & Hello command handler
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

# Horoscope command handler
@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)

# Ask for the day
def day_handler(message):
    sign = message.text.strip()
    text = "What day do you want the horoscope for?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date (YYYY-MM-DD)."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, fetch_horoscope, sign.capitalize())

# Fetch and send horoscope
def fetch_horoscope(message, sign):
    day = message.text.strip().upper()
    horoscope = get_daily_horoscope(sign, day)
    
    if horoscope.get("success"):
        data = horoscope["data"]
        horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
        bot.send_message(message.chat.id, "Here's your horoscope!")
        bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "Sorry, I couldn't fetch your horoscope. Please try again.")

# Set of known commands
KNOWN_COMMANDS = {"/start", "/hello", "/horoscope"}

# Unknown command handler
@bot.message_handler(func=lambda message: message.text.startswith("/") and message.text not in KNOWN_COMMANDS)
def unknown_command(message):
    bot.reply_to(message, "Sorry, I don't understand that command. Try /start, /hello, or /horoscope.")

# Run bot
bot.infinity_polling(timeout=10, long_polling_timeout=5)

