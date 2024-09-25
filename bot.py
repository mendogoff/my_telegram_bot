import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging
import asyncio

# Логирование
logging.basicConfig(level=logging.INFO)

# Получаем токен бота из переменной окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = "https://your_public_url/webhook/"  # Ваш публичный URL для вебхука

# Инициализация Flask приложения
app = Flask(__name__)

# Инициализация Telegram Bot API
bot = Bot(token=TOKEN)
application = Application.builder().token(TOKEN).build()

# Список для хранения участников чата
chat_participants = {}

# Команда /start - регистрация нового пользователя в чате
async def start(update: Update, context):
    user_id = update.message.from_user.id
    chat_participants[user_id] = update.message.from_user.first_name
    await update.message.reply_text("Вы присоединились к анонимному чату. Все ваши сообщения будут отправлены анонимно.")

# Обработчик текстовых сообщений - пересылка сообщений всем участникам чата
async def handle_message(update: Update, context):
    user_id = update.message.from_user.id
    text = update.message.text
    
    # Анонимное сообщение для всех участников, кроме отправителя
    for participant_id in chat_participants:
        if participant_id != user_id:
            await bot.send_message(chat_id=participant_id, text=f"Аноним: {text}")

# Команда /help
async def help_command(update: Update, context):
    await update.message.reply_text("Используйте /start для входа в анонимный чат. Все ваши сообщения будут отправляться анонимно другим участникам.")

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
    """Получение обновлений от Telegram через вебхук."""
    update = Update.de_json(request.get_json(), bot)
    await application.process_update(update)
    return "ok", 200

if __name__ == '__main__':
    # Установка вебхука при запуске
    asyncio.run(set_webhook())
    # Запуск Flask-сервера
    app.run(debug=False, host='0.0.0.0', port=10000)
