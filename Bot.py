import os
import requests
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

def send_message(chat_id, text, keyboard=None):
    data = {
        "chat_id": chat_id,
        "text": text
    }
    if keyboard:
        data["reply_markup"] = keyboard
    requests.post(f"{API}/sendMessage", json=data)

def menu():
    return {
        "keyboard": [
            [{"text": "📋 Техкарты"}],
            [{"text": "⚖️ Рассчитать сырьё"}],
            [{"text": "💰 Себестоимость"}]
        ],
        "resize_keyboard": True
    }

@app.route("/", methods=["POST"])
def webhook():
    data = request.json

    if "message" not in data:
        return "OK"

    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        send_message(
            chat_id,
            "👋 Добро пожаловать!\n\n"
            "🏭 Бот производственных техкарт\n\n"
            "Выберите действие:",
            menu()
        )

    elif text == "📋 Техкарты":
        send_message(
            chat_id,
            "📋 ТЕХКАРТЫ\n\n"
            "Пока здесь будет список твоих изделий.\n\n"
            "Например:\n"
            "🥟 Барак\n"
            "🥐 Слойка\n"
            "🥟 Самса\n\n"
            "Дальше мы добавим реальные техкарты."
        )

    elif text == "⚖️ Рассчитать сырьё":
        send_message(
            chat_id,
            "⚖️ РАСЧЁТ СЫРЬЯ\n\n"
            "Здесь бот будет пересчитывать техкарту "
            "на любое количество продукции.\n\n"
            "Например: 300 кг → сколько нужно каждого сырья."
        )

    elif text == "💰 Себестоимость":
        send_message(
            chat_id,
            "💰 СЕБЕСТОИМОСТЬ\n\n"
            "Здесь добавим цены сырья и расчёт "
            "себестоимости 1 кг и 1 штуки."
        )

    else:
        send_message(
            chat_id,
            "Выберите действие из меню 👇",
            menu()
        )

    return "OK"

@app.route("/", methods=["GET"])
def home():
    return "Tex-kart bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
