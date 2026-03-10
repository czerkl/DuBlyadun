# -*- coding: utf-8 -*-
import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command
from src.config import config
from src.database.supabase_client import db
from src.services.groq_service import ai_manager
from src.services.logger_service import send_log

router = Router()

# --- АДМИН ПАНЕЛЬ ---

@router.message(Command("change"))
async def cmd_change_model(message: types.Message):
    """Команда для смены модели ИИ"""
    if message.from_user.id != config.ADMIN_ID: return
    
    args = message.text.split()
    if len(args) < 2:
        current = ai_manager.current_model
        text = (
            f"🤖 <b>Текущая модель:</b> <code>{current}</code>\n\n"
            f"<b>Доступные варианты:</b>\n"
            f"1. <code>llama-3.1-8b-instant</code> (Быстрая)\n"
            f"2. <code>llama-3.1-70b-versatile</code> (Умная)\n"
            f"3. <code>mixtral-8x7b-32768</code> (Баланс)\n\n"
            f"Чтобы сменить, напиши: <code>/change название_модели</code>"
        )
        await message.reply(text, parse_mode="HTML")
        return

    new_model = args[1].strip()
    ai_manager.current_model = new_model
    await message.reply(f"✅ Модель успешно изменена на: <code>{new_model}</code>", parse_mode="HTML")
    await send_log(message.bot, f"Админ сменил модель на: {new_model}")

@router.message(Command("prompt"))
async def cmd_set_prompt(message: types.Message):
    """Команда для смены личности"""
    if message.from_user.id != config.ADMIN_ID: return
    new_p = message.text.replace("/prompt", "").strip()
    if not new_p:
        await message.reply(f"Текущая личность:\n<code>{ai_manager.system_prompt}</code>", parse_mode="HTML")
        return
    ai_manager.system_prompt = new_p
    await message.reply("✅ Личность Дурова обновлена.")

@router.message(Command("clear"))
async def cmd_clear(message: types.Message):
    await asyncio.to_thread(db.clear_history, message.chat.id)
    await message.reply("🧹 Память этого чата очищена.")

# --- ГЛАВНЫЙ ОБРАБОТЧИК ---

@router.message(F.text)
async def handle_messages(message: types.Message):
    # Проверка на триггеры
    is_hit = any(word in message.text.lower() for word in ["дуров", "блядун", "паша", "павел"])
    is_reply = message.reply_to_message and message.reply_to_message.from_user.id == message.bot.id
    is_private = message.chat.type == "private"

    if is_hit or is_reply or is_private:
        chat_id = message.chat.id
        try:
            await message.bot.send_chat_action(chat_id, action="typing")
            
            # Загружаем историю и генерируем ответ
            history = await asyncio.to_thread(db.get_history, chat_id)
            response_text = await ai_manager.get_durov_response(history + [{"role": "user", "content": message.text}])
            
            await message.reply(response_text)

            # Сохраняем в базу
            await asyncio.to_thread(db.save_message, chat_id, "user", message.text)
            await asyncio.to_thread(db.save_message, chat_id, "assistant", response_text)
            
            # Логируем
            await send_log(message.bot, f"User: {message.from_user.id}\nModel: {ai_manager.current_model}\nText: {message.text[:50]}...")
            
        except Exception as e:
            await send_log(message.bot, f"Error: {e}")
            await message.reply("Паша занят, попробуй позже.")
