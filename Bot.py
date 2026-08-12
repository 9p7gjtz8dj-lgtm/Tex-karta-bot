import os
import time
import threading
import requests
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("Не найден BOT_TOKEN")

API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)


@app.route("/")
def home():
    return "Tex-karta bot is running!"


def send_message(chat_id, text):
    requests.post(
        f"{API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        },
        timeout=30
    )


def telegram_bot():
    offset = 0

    while True:
        try:
            response = requests.get(
                f"{API}/getUpdates",
                params={
                    "offset": offset,
                    "timeout": 30
                },
                timeout=35
            )

            data = response.json()

            for update in data.get("result", []):
                offset = update["update_id"] + 1

                message = update.get("message")
                if not message:
                    continue

                chat_id = message["chat"]["id"]
                text = message.get("text", "").strip()

                if text == "/start":
                    send_message(
                        chat_id,
                        "👋 Привет!\n\n"
                        "Я бот для техкарт.\n\n"
                        "Команды:\n"
                        "/start — начать\n"
                        "/help — помощь\n"
                        "/calc — расчёт количества сырья\n\n"
                        "Сейчас можем сделать расчёт техкарты."
                    )

                elif text == "/help":
                    send_message(
                        chat_id,
                        "📋 Помощь\n\n"
                        "Напиши /calc и я помогу пересчитать "
                        "сырьё на нужное количество продукции."
                    )

                elif text == "/calc":
                    send_message(
                        chat_id,
                        "🧮 Расчёт техкарты\n\n"
                        "Напиши исходный выход и нужный выход.\n\n"
                        "Например:\n"
                        "Исходный выход: 10 кг\n"
                        "Нужный выход: 3 кг"
                    )

                else:
                    send_message(
                        chat_id,
                        "Я получил сообщение 👍\n\n"
                        "Используй /start или /calc."
                    )

        except Exception as e:
            print("Ошибка:", e)
            time.sleep(5)


if __name__ == "__main__":
    threading.Thread(target=telegram_bot, daemon=True).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
