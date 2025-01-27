#pip install requests
#pip install pyTelegramBotAPI

import telebot
import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
    'Content-Type': 'application/json',
}
#برای ایجاد یک بات تلگرام میتونید از Botfather در خود تلگرام این کار رو بکنید ، توکن بات رو اینجا قرار بدید و بات رو استارت کنید ، بعد پروژه رو ران کنید و /start رو بزنید و تمام :)
API_TOKEN = 'بات توکن خودتون رو اینجا وارد کنید !'
bot = telebot.TeleBot(API_TOKEN)
url = 'https://price.tlyn.ir/api/v1/price'
response = requests.get(url, headers=headers)
prices = response.json()['prices']
buttons = {
    "گرم طلا عیار ۱۸": None,
    "مظنه - مثقال عیار ۱۷": None,
    "سکه تمام": None,
    "نیم سکه": None,
    "ربع سکه": None
}
def get_price(price_title):
    for price in prices:
        if price['title'] == price_title:
            sell_price = price['price']['sell'] * 1000  # تبدیل به ریال
            buy_price = price['price']['buy'] * 1000    # تبدیل به ریال
            return f"{price_title}:\n\nفروش: {sell_price:,} تومان\nخرید: {buy_price:,} تومان"


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button in buttons:
        markup.add(button)
    bot.send_message(message.chat.id, "سلام! لطفاً دکمه مورد نظر را انتخاب کنید:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text in buttons:
        price_message = get_price(message.text)
        bot.send_message(message.chat.id, price_message)

bot.polling()
