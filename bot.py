import logging
from flask import Flask, request, render_template
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
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
TOKEN = "Ваш_токен_бота"
CHANNEL_ID = -362309632

# Хранилище объявлений (в памяти)
ads_storage = []

@app.route('/')
def home():
    """Главная страница с интерфейсом"""
    return render_template('index.html', ads=ads_storage)

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

async def run_bot():
    """Запуск Telegram-бота"""
    logger.info("Запуск телеграм-бота")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("add", add))  # Оставляем обработку команды /add
    await application.run_polling()

if __name__ == "__main__":
    logger.info("Запуск Flask-приложения и бота")
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
