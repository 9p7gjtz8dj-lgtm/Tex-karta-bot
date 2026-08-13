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

                # START
                if text == "/start":
                    send_message(
                        chat_id,
                        "👋 Привет!\n\n"
                        "Я бот для техкарт.\n\n"
                        "Просто отправь мне техкарту в таком виде:\n\n"
                        "Сомса\n"
                        "Мясо 300\n"
                        "Вода 200\n"
                        "Лук 100"
                    )

                # HELP
                elif text == "/help":
                    send_message(
                        chat_id,
                        "📋 Помощь\n\n"
                        "Отправь техкарту:\n\n"
                        "Сомса\n"
                        "Мясо 300\n"
                        "Вода 200\n"
                        "Лук 100"
                    )

                # ОБРАБОТКА ТЕХКАРТЫ
                else:
                    lines = text.splitlines()

                    if len(lines) >= 2:
                        product_name = lines[0].strip()
                        ingredients = []
                        total = 0

                        for line in lines[1:]:
                            parts = line.rsplit(" ", 1)

                            if len(parts) == 2:
                                ingredient = parts[0].strip()

                                try:
                                    amount = float(
                                        parts[1].replace(",", ".")
                                    )

                                    ingredients.append(
                                        (ingredient, amount)
                                    )

                                    total += amount

                                except ValueError:
                                    pass

                        if ingredients:
                            result = f"✅ Техкарта: {product_name}\n\n"

                            for ingredient, amount in ingredients:
                                if amount.is_integer():
                                    amount_text = str(int(amount))
                                else:
                                    amount_text = str(amount)

                                result += f"{ingredient} — {amount_text}\n"

                            result += f"\n⚖️ Общая масса: {total:g}"

                            send_message(chat_id, result)

                        else:
                            send_message(
                                chat_id,
                                "❌ Не смог распознать ингредиенты.\n\n"
                                "Пример:\n"
                                "Сомса\n"
                                "Мясо 300\n"
                                "Вода 200\n"
                                "Лук 100"
                            )

                    else:
                        send_message(
                            chat_id,
                            "❌ Напиши техкарту в таком формате:\n\n"
                            "Сомса\n"
                            "Мясо 300\n"
                            "Вода 200\n"
                            "Лук 100"
                        )

        except Exception as e:
            print("Ошибка:", e)
            time.sleep(5)


if __name__ == "__main__":
    threading.Thread(
        target=telegram_bot,
        daemon=True
    ).start()

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
