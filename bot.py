import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

# Включаем логирование для отладки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем токен и ID канала из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8027225541:AAFUq7VeX9zWHHfnISipKM53nZgi4s7_odg")
CHANNEL_ID = os.getenv("CHANNEL_ID", "-1002388187883")

# URL для вебхука
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Установи его в настройках Render/Heroku

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправьте мне сообщение, и я опубликую его в канале анонимно.")

# Функция для обработки обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text  # Текст сообщения от пользователя

    # Отправляем сообщение в канал от имени бота
    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=f"📝 Анонимное сообщение:\n\n{user_message}"
    )

    # Подтверждаем отправку пользователю
    await update.message.reply_text("Ваше сообщение было отправлено в канал анонимно!")

# Функция для обработки ошибок
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f'Произошла ошибка: {context.error}')

def main():
    # Инициализация приложения с вашим токеном
    application = Application.builder().token(TOKEN).build()

    # Обработчик для команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик для всех текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Логируем ошибки
    application.add_error_handler(error_handler)

    # Установка вебхуков
    application.run_webhook(
        listen="0.0.0.0",  # Слушаем на всех интерфейсах
        port=int(os.getenv("PORT", 8443)),  # Порт из переменной окружения
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"  # URL вебхука
    )

if __name__ == '__main__':
    main()
