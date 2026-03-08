import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command
from src.database.supabase_client import db
from src.services.groq_service import ai_manager
from src.services.logger_service import send_log

router = Router()

# Хендлер на команду /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        "Приватность — это не право на секреты, это право на индивидуальность. "
        "Я здесь. Пиши 'Дуров', если возникнут вопросы по делу."
    )
    await message.answer(welcome_text)

# Основной хендлер на текст
@router.message(F.text)
async def handle_all_messages(message: types.Message):
    if message.from_user.is_bot:
        return

    text = message.text.lower()
    # Твои триггеры в малом регистре
    triggers = ["дуров", "блядун", "паша", "павел"]
    is_hit = any(word in text for word in triggers)
    
    # Ответ, если тегнули бота или ответили на его сообщение
    is_reply = message.reply_to_message and message.reply_to_message.from_user.id == message.bot.id
    
    # В ЛИЧКЕ бот должен отвечать на всё, в ГРУППАХ - только на триггеры
    is_private = message.chat.type == "private"

    if is_hit or is_reply or is_private:
        chat_id = message.chat.id
        await message.bot.send_chat_action(chat_id, action="typing")

        # Достаем историю из Supabase
        history = await asyncio.to_thread(db.get_history, chat_id)
        history.append({"role": "user", "content": message.text})

        # Получаем ответ от ИИ (там уже вшита харизма на случай ошибок)
        response_text = await ai_manager.get_durov_response(history)

        await message.reply(response_text)

        # Сохраняем всё это дело
        await asyncio.to_thread(db.save_message, chat_id, "user", message.text)
        await asyncio.to_thread(db.save_message, chat_id, "assistant", response_text)
        
        # Лог в канал
        log_msg = f"User: {message.from_user.full_name}\nTxt: {message.text}\nAns: {response_text}"
        await send_log(message.bot, log_msg)