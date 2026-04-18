import telebot
import requests

TOKE8333783224:AAGQJWzei5htTvJArTmdSX0_KmtEU8JBxQs

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text'])
def reply(message):
    text = message.text

    # ساخت عکس
    if text.startswith("/img"):
        prompt = text.replace("/img", "")

        url = "https://api.openai.com/v1/images"
        headers = {
            "Authorization": f"Bearer {OPENAI_API}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-image-1",
            "prompt": prompt,
            "size": "1024x1024"
        }

        try:
            res = requests.post(url, headers=headers, json=data)
            image_url = res.json()["data"][0]["url"]
            bot.send_photo(message.chat.id, image_url)
        except:
            bot.reply_to(message, "خطا در ساخت عکس")

    # جواب سوال
    else:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": text}]
        }

        try:
            res = requests.post(url, headers=headers, json=data)
            answer = res.json()["choices"][0]["message"]["content"]
            bot.reply_to(message, answer)
        except:
            bot.reply_to(message, "خطا شد دوباره امتحان کن")

bot.infinity_polling()
