import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command
from src.config import config
from src.database.supabase_client import db
from src.services.groq_service import ai_manager
from src.services.logger_service import send_log

router = Router()

@router.message(Command("prompt"))
async def cmd_set_prompt(message: types.Message):
    if message.from_user.id != config.ADMIN_ID: return
    new_p = message.text.replace("/prompt", "").strip()
    if not new_p:
        await message.reply(f"Текущий промпт:\n<code>{ai_manager.system_prompt}</code>", parse_mode="HTML")
        return
    ai_manager.system_prompt = new_p
    await message.reply("✅ Личность Дурова обновлена.")

@router.message(Command("clear"))
async def cmd_clear_history(message: types.Message):
    await asyncio.to_thread(db.clear_history, message.chat.id)
    await message.reply("🧹 Память стерта. Кто ты?")

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
            # 1. Сразу сохраняем входящее сообщение
            await asyncio.to_thread(db.save_message, chat_id, "user", message.text)
            await message.bot.send_chat_action(chat_id, action="typing")

            # 2. Получаем историю (включая только что сохраненное сообщение)
            history = await asyncio.to_thread(db.get_history, chat_id)

            # 3. Генерация ответа через Groq
            response_text = await ai_manager.get_durov_response(history)
            await message.reply(response_text)

            # 4. Сохраняем ответ бота
            await asyncio.to_thread(db.save_message, chat_id, "assistant", response_text)

            # 5. Логирование
            await send_log(message.bot, f"User: {message.from_user.full_name}\nTxt: {message.text}\nAns: {response_text}")

        except Exception as e:
            await send_log(message.bot, f"⚠️ ОШИБКА: {type(e).__name__}\n{str(e)}")
            await message.reply("Система перегружена. Паша ушел в горы.")
