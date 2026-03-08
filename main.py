import asyncio
import logging
from aiogram import Bot, Dispatcher
from src.config import config
from src.handlers.messages import router
from src.server import start_web_server
from src.services.logger_service import send_log

# Настройка логирования (чтобы видеть, что происходит в консоли Render)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

async def main():
    # 1. Инициализация бота и диспетчера
    bot = Bot(token=config.TG_TOKEN)
    dp = Dispatcher()

    # 2. Подключаем маршруты (команды /start, триггеры "Дуров" и т.д.)
    dp.include_router(router)

    # 3. Сообщение в твой лог-канал о том, что бот успешно ожил
    await send_log(bot, "🚀 <b>Система 'Дуров Блядун' v1.2 запущена.</b>\nСтатус: Мониторинг активен.")

    try:
        logging.info("--- Бот запущен и слушает сообщения ---")
        
        # 4. Запускаем всё параллельно:
        # - dp.start_polling: слушает Telegram
        # - start_web_server: отвечает пингеру Google, чтобы Render не спал
        await asyncio.gather(
            dp.start_polling(bot),
            start_web_server()
        )
    except Exception as e:
        # Если что-то упадет, ты увидишь ошибку в логах Render
        logging.error(f"Критическая ошибка при работе бота: {e}")
        await send_log(bot, f"⚠️ <b>Критическая ошибка:</b>\n<code>{e}</code>")
    finally:
        # Важно: закрываем сессию бота, чтобы не было утечек памяти
        await bot.session.close()
        logging.info("--- Сессия бота закрыта ---")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен пользователем.")