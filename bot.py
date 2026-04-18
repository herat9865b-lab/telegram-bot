import telebot
import requests

# 🔴 توکن ربات تلگرام
TOKEN = 8681581969:AAH5187dNms3ANLj3SoB5HpRKnI78ZZtO1I

# 🔴 API هوش مصنوعی
OPENAI_API_KEY = "PUT_YOUR_OPENAI_KEY"

bot = telebot.TeleBot(TOKEN)

# =========================
# 🔹 جواب سوال (چت)
def chat_ai(text):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "تو یک ربات فارسی هستی، کوتاه و خوب جواب بده"},
            {"role": "user", "content": text}
        ]
    }

    res = requests.post(url, headers=headers, json=data)
    return res.json()["choices"][0]["message"]["content"]

# =========================
# 🔹 ساخت عکس
def generate_image(prompt):
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": "1024x1024"
    }

    res = requests.post(url, headers=headers, json=data)
    return res.json()["data"][0]["url"]

# =========================
# 🔹 شروع
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "سلام 👋\n\nبرای سوال بنویس ✍️\nبرای عکس بنویس:\n/تصویر گربه")

# =========================
# 🔹 دریافت پیام
@bot.message_handler(func=lambda message: True)
def handle(message):
    text = message.text

    try:
        # اگر دستور عکس بود
        if text.startswith("/تصویر"):
            prompt = text.replace("/تصویر", "").strip()
            bot.reply_to(message, "در حال ساخت عکس... 🎨")
            img_url = generate_image(prompt)
            bot.send_photo(message.chat.id, img_url)

        else:
            reply = chat_ai(text)
            bot.reply_to(message, reply)

    except Exception as e:
        bot.reply_to(message, "خطا ❌ دوباره امتحان کن")

# =========================
print("Bot is running...")
bot.infinity_polling()
