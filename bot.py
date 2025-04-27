from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

# Получаем токен и ID канала из переменных окружения
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Функция для генерации хэштегов
def generate_hashtags(data):
    hashtags = []
    for word in data.split():
        if word.isdigit():  # Если это число (например, год или цена)
            hashtags.append(f"#{word}")
        else:  # Если это текст (например, марка или модель)
            hashtags.append(f"#{word.capitalize()}")
    return " ".join(hashtags)

# Команда для добавления объявления
def add(update: Update, context: CallbackContext):
    user = update.effective_user
    if not context.args:
        update.message.reply_text("Пожалуйста, отправьте данные в формате: Марка, Модель, Год, Цена")
        return

    # Формируем текст объявления
    ad_text = f"🚗 Новое объявление от @{user.username or user.first_name}:\n" \
              f"{' '.join(context.args)}"

    # Генерируем хэштеги
    hashtags = generate_hashtags(' '.join(context.args))

    # Отправляем объявление в канал
    bot = Bot(TOKEN)
    bot.send_message(chat_id=CHANNEL_ID, text=f"{ad_text}\n\n{hashtags}")

    update.message.reply_text("Ваше объявление успешно добавлено!")

# Основная функция
def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("add", add))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()