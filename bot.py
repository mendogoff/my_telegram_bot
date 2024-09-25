import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os
from flask import Flask, request

# Включаем логирование для отладки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем токен и ID канала из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8027225541:AAFUq7VeX9zWHHfnISipKM53nZgi4s7_odg")
CHANNEL_ID = os.getenv("CHANNEL_ID", "-1002388187883")  # Ваш ID канала

# Flask-приложение для вебхуков
app = Flask(__name__)

# Функция для обработки команды /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Отправьте мне сообщение, и я опубликую его в канале анонимно.")

# Функция для обработки обычных сообщений
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text  # Текст сообщения от пользователя

    # Отправляем сообщение в канал от имени бота
    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=f"📝 Анонимное сообщение:\n\n{user_message}"
    )

    # Подтверждаем отправку пользователю
    await update.message.reply_text("Ваше сообщение было отправлено в канал анонимно!")

# Функция для обработки ошибок
async def error_handler(update: object, context: CallbackContext):
    logger.error(f'Произошла ошибка: {context.error}')

# Обработка вебхуков через Flask
@app.route('/webhook/', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(), application.bot)
        application.process_update(update)
        return 'ok', 200

def main():
    # Инициализация приложения с вашим токеном
    global application
    application = Application.builder().token(TOKEN).build()

    # Обработчик для команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик для всех текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Логируем ошибки
    application.add_error_handler(error_handler)

    # Устанавливаем вебхук
    application.bot.set_webhook(url="https://telegram-bot.onrender.com/webhook/")  # URL вебхука
    
    # Запуск Flask-сервера
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == '__main__':
    main()



