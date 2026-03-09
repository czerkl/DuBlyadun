import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command
from src.config import config
from src.database.supabase_client import db
from src.services.groq_service import ai_manager
from src.services.logger_service import send_log

router = Router()

@router.message(Command("change"))
async def cmd_change_model(message: types.Message):
    if message.from_user.id != config.ADMIN_ID:
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.reply(f"текущая модель: {ai_manager.current_model}")
        return
    ai_manager.current_model = parts[1]
    await message.reply(f"модель изменена на {parts[1]}")

@router.message(F.text)
async def handle_all_messages(message: types.Message):
    if message.from_user.is_bot: return

    text = message.text.lower()
    triggers = ["дуров", "блядун", "паша", "павел"]
    is_hit = any(word in text for word in triggers)
    is_reply = message.reply_to_message and message.reply_to_message.from_user.id == message.bot.id
    is_private = message.chat.type == "private"

    if is_hit or is_reply or is_private:
        chat_id = message.chat.id
        try:
            await message.bot.send_chat_action(chat_id, action="typing")

            # 1. Получаем историю
            history = await asyncio.to_thread(db.get_history, chat_id)
            history.append({"role": "user", "content": message.text})

            # 2. Ответ от ИИ
            response_text = await ai_manager.get_durov_response(history)
            await message.reply(response_text)

            # 3. Сохраняем
            await asyncio.to_thread(db.save_message, chat_id, "user", message.text)
            await asyncio.to_thread(db.save_message, chat_id, "assistant", response_text)

        except Exception as e:
            # ВОТ ТУТ МАГИЯ: любой сбой летит в лог-канал
            error_msg = f"Ошибка в чате {chat_id}: {str(e)}"
            await send_log(message.bot, error_msg)
            
            # Ответ пользователю, чтобы не было тишины
            if "rate_limit" in str(e).lower() or "429" in str(e):
                await message.reply("лимиты исчерпаны. отдохни.")
            else:
                await message.reply("что-то пошло не так. глянь логи.")
