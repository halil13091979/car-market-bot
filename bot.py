from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
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
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not context.args:
        await update.message.reply_text("Пожалуйста, отправьте данные в формате: Марка, Модель, Год, Цена")
        return

    # Формируем текст объявления
    ad_text = f"🚗 Новое объявление от @{user.username or user.first_name}:\n" \
              f"{' '.join(context.args)}"

    # Генерируем хэштеги
    hashtags = generate_hashtags(' '.join(context.args))

    # Отправляем объявление в канал
    bot = Bot(TOKEN)
    await bot.send_message(chat_id=CHANNEL_ID, text=f"{ad_text}\n\n{hashtags}")

    await update.message.reply_text("Ваше объявление успешно добавлено!")

# Основная функция
def main():
    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчик команды /add
    application.add_handler(CommandHandler("add", add))

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
