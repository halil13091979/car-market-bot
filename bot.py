import logging
from flask import Flask, request
from telegram import Bot
import os
import asyncio

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask-приложение
app = Flask(__name__)

# Telegram настройки
TOKEN = "7807736400:AAFCb_0m79n603AmL6Q9UDtIBxQ0m2m2rCc"
CHANNEL_ID = "-1002630184427"
# Хранилище объявлений (в памяти)
ads_storage = []

@app.route('/')
def home():
    """Главная страница с интерфейсом"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Car Market Bot</title>
    </head>
    <body>
        <h1>Car Market Bot</h1>
        <h2>Добавить объявление:</h2>
        <form method="POST" action="/add_ad">
            <textarea name="data" rows="4" cols="50" placeholder="Введите данные объявления"></textarea>
            <br>
            <button type="submit">Добавить</button>
        </form>
        <h2>Отправленные объявления:</h2>
        <ul>
    """
    for ad in ads_storage:
        html_content += f"<li>{ad}</li>"
    html_content += """
        </ul>
    </body>
    </html>
    """
    return html_content

@app.route('/add_ad', methods=['POST'])
def add_ad():
    """Обработка формы для добавления объявления"""
    data = request.form.get("data")
    if not data:
        return "Ошибка: данные не предоставлены", 400

    hashtags = generate_hashtags(data)
    ad_text = f"🚗 Новое объявление:\n{data}\n\n{hashtags}"
    ads_storage.append(ad_text)

    # Отправка в Telegram
    try:
        bot = Bot(TOKEN)
        bot.send_message(chat_id=CHANNEL_ID, text=ad_text)
        logger.info("Объявление отправлено в канал")
    except Exception as e:
        logger.error("Ошибка при отправке сообщения: %s", e)
        return "Ошибка при отправке объявления", 500

    return "Объявление успешно добавлено!", 200

def generate_hashtags(data):
    """Генерация хэштегов"""
    logger.info("Генерация хэштегов для данных: %s", data)
    hashtags = []
    for word in data.split():
        if word.isdigit():
            hashtags.append(f"#{word}")
        else:
            hashtags.append(f"#{word.capitalize()}")
    return " ".join(hashtags)

if __name__ == "__main__":
    logger.info("Запуск Flask-приложения")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
