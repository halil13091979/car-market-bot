from flask import Flask
from threading import Thread
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# Flask-приложение
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

# Получаем токен и ID канала из переменных окружения
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Функция для генерации хэштегов
def generate_hashtags(data):
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
    if not context.args:
        await update.message.reply_text("Пожалуйста, отправьте данные в формате: Марка, Модель, Год, Цена")
        return

    ad_text = f"🚗 Новое объявление от @{user.username or user.first_name}:\n" \
              f"{' '.join(context.args)}"

    hashtags = generate_hashtags(' '.join(context.args))

    bot = Bot(TOKEN)
    await bot.send_message(chat_id=CHANNEL_ID, text=f"{ad_text}\n\n{hashtags}")

    await update.message.reply_text("Ваше объявление успешно добавлено!")

# Основная функция
def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("add", add))
    application.run_polling()

# Запуск бота в отдельном потоке
def start_bot():
    thread = Thread(target=run_bot)
    thread.start()

if __name__ == "__main__":
    start_bot()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))  # Запуск Flask-сервера
