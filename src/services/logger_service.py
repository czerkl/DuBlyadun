from aiogram import Bot
from src.config import config

async def send_log(bot: Bot, message: str):
    """Отправляет лог в твой приватный канал"""
    if config.LOG_CHAT_ID:
        try:
            # Форматируем лог, чтобы он выглядел красиво
            text = f"<b>[LOG]</b>\n<code>{message}</code>"
            await bot.send_message(chat_id=config.LOG_CHAT_ID, text=text, parse_mode="HTML")
        except Exception as e:
            print(f"Не удалось отправить лог: {e}")