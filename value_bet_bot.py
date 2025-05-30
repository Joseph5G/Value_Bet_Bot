
import requests
from bs4 import BeautifulSoup
import telebot
import schedule
import time
import datetime
import pytz

# Your credentials
BOT_TOKEN = '8053238815:AAFVlLJOWGpxo2t9BufZa4fmhgQ0JTdsfVE'
CHAT_ID = 'REPLACE_WITH_YOUR_CHAT_ID'  # Replace this after running the ID script
bot = telebot.TeleBot(BOT_TOKEN)

def get_value_bets():
    url = "https://www.predictz.com/predictions/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    predictions = soup.find_all("div", class_="six columns")[:5]  # First 5 predictions
    bets = []

    for pred in predictions:
        match = pred.find("h2").text.strip() if pred.find("h2") else "Unknown Match"
        pick = pred.find("strong").text.strip() if pred.find("strong") else "No Tip"
        odds = pred.find("span", class_="odds")
        odds_text = odds.text.strip() if odds else "N/A"
        bets.append(f"🏟 {match}\n💰 Tip: {pick}\n📈 Odds: {odds_text}")

    return bets

def send_daily_bets():
    bets = get_value_bets()
    if bets:
        today = datetime.date.today().strftime('%Y-%m-%d')
        message = f"🎯 *Value Bets for {today}*\n\n" + "\n\n".join(bets)
        bot.send_message(CHAT_ID, message, parse_mode="Markdown")
    else:
        bot.send_message(CHAT_ID, "No value bets found today.")

def run_daily():
    nigeria_time = pytz.timezone("Africa/Lagos")
    now = datetime.datetime.now(nigeria_time)
    if now.hour == 11 and now.minute == 0:
        send_daily_bets()

schedule.every().minute.do(run_daily)

print("Bot is running...")

while True:
    schedule.run_pending()
    time.sleep(30)
