import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging
import asyncio

# Логирование
logging.basicConfig(level=logging.INFO)

# Получаем токен бота и ID канала из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Убедитесь, что в вашем окружении есть переменная TELEGRAM_BOT_TOKEN
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")  # Убедитесь, что в вашем окружении есть переменная TELEGRAM_CHANNEL_ID
WEBHOOK_URL = "https://api.render.com/deploy/srv-crq8k7l2ng1s73e46h40?key=rdyLgUfDFm4/webhook/"  # Ваш публичный URL для вебхука

# Инициализация Flask приложения
app = Flask(__name__)

# Инициализация Telegram Bot API
bot = Bot(token=TOKEN)
application = Application.builder().token(TOKEN).build()

# Команда /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Вы можете отправлять анонимные сообщения, которые будут пересылаться в канал.")

# Обработчик текстовых сообщений - пересылка сообщений в канал
async def handle_message(update: Update, context):
    text = update.message.text
    message_to_send = f"Сообщение от анонима: {text}"
    
    # Отправляем сообщение в канал
    await bot.send_message(chat_id=CHANNEL_ID, text=message_to_send)
    
    # Подтверждаем отправку пользователю
    await update.message.reply_text("Ваше сообщение было отправлено в канал анонимно.")

# Команда /help
async def help_command(update: Update, context):
    await update.message.reply_text("Используйте /start для начала отправки сообщений в анонимный канал.")

# Добавляем обработчики команд и сообщений
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Установка вебхука
async def set_webhook():
    await bot.set_webhook(url=WEBHOOK_URL)

# Обработчик вебхуков
@app.route('/webhook/', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(), bot)
    await application.process_update(update)
    return "ok", 200

if __name__ == '__main__':
    # Установка вебхука при запуске
    asyncio.run(set_webhook())
    # Запуск Flask-сервера
    app.run(debug=False, host='0.0.0.0', port=10000)
