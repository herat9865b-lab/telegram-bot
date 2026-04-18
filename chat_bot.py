import telebot
import requests

TOKEN = 8681581969:AAH5187dNms3ANLj3SoB5HpRKnI78ZZtO1I

bot = telebot.TeleBot(TOKEN)

# محدودیت ساده
users = {}

def check_limit(user_id):
    if user_id not in users:
        users[user_id] = 0
    if users[user_id] >= 10:
        return False
    users[user_id] += 1
    return True

# جواب سوال (سبک)
def ai_reply(text):
    r = requests.post(
        "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
        json={"inputs": text}
    )
    try:
        return r.json()[0]["generated_text"]
    except:
        return "دوباره بپرس 😅"

# ساخت عکس (سبک)
def ai_image(prompt):
    return f"https://image.pollinations.ai/prompt/{prompt}"

# دستور سوال
@bot.message_handler(commands=['ask'])
def ask(message):
    if not check_limit(message.chat.id):
        bot.reply_to(message, "امروز حدت تمام شد 😐")
        return

    text = message.text.replace("/ask ", "")
    answer = ai_reply(text)
    bot.reply_to(message, answer)

# دستور عکس
@bot.message_handler(commands=['img'])
def img(message):
    if not check_limit(message.chat.id):
        bot.reply_to(message, "امروز حدت تمام شد 😐")
        return

    prompt = message.text.replace("/img ", "")
    url = ai_image(prompt)
    bot.send_photo(message.chat.id, url)

# پیام عادی
@bot.message_handler(func=lambda m: True)
def normal(message):
    if not check_limit(message.chat.id):
        bot.reply_to(message, "امروز حدت تمام شد 😐")
        return

    answer = ai_reply(message.text)
    bot.reply_to(message, answer)

print("Bot is running...")
bot.infinity_polling()
