import logging
from flask import Flask
from telegram import Update, Bot
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

@app.route('/')
def home():
    logger.info("Главная страница Flask была вызвана")
    return "Бот работает!"

# Правильный формат токена
TOKEN = "7807736400:AAFCb_0m79n603AmL6Q9UDtIBxQ0m2m2rCc"
CHANNEL_ID = -362309632  # ID канала должен быть числом

# Функция для генерации хэштегов
def generate_hashtags(data):
    logger.info("Генерация хэштегов для данных: %s", data)
    hashtags = []
    for word in data.split():
        if word.isdigit():
            hashtags.append(f"#{word}")
        else:
            hashtags.append(f"#{word.capitalize()}")
    return " ".join(hashtags)

# Команда для добавления объявления
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info("Команда /add вызвана пользователем: %s", user.username or user.first_name)
    
    if not context.args:
        logger.warning("Пользователь не предоставил аргументы для команды /add")
        await update.message.reply_text("Пожалуйста, отправьте данные в формате: Марка, Модель, Год, Цена")
        return

    ad_text = f"🚗 Новое объявление от @{user.username or user.first_name}:\n" \
              f"{' '.join(context.args)}"
    hashtags = generate_hashtags(' '.join(context.args))

    try:
        bot = Bot(TOKEN)
        await bot.send_message(chat_id=CHANNEL_ID, text=f"{ad_text}\n\n{hashtags}")
        logger.info("Объявление отправлено в канал: %s", CHANNEL_ID)
        await update.message.reply_text("Ваше объявление успешно добавлено!")
    except Exception as e:
        logger.error("Ошибка при отправке сообщения: %s", e)
        await update.message.reply_text("Произошла ошибка при добавлении объявления.")

# Основная функция для запуска бота
async def run_bot():
    logger.info("Запуск телеграм-бота")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("add", add))
    await application.run_polling()

if __name__ == "__main__":
    # Запускаем Flask и бота параллельно
    logger.info("Запуск Flask-приложения и бота")
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
