# -*- coding: utf-8 -*-
import asyncio
import logging
from aiogram import Bot, Dispatcher
from src.config import config
from src.handlers.messages import router
from src.server import start_web_server
from src.services.logger_service import send_log

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

async def main():
    bot = Bot(token=config.TG_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    # Упростил текст, чтобы убрать возможные ошибки кодировки
    await send_log(bot, "System Online: Durov v2.0 is active.")

    try:
        logging.info("--- Бот запущен ---")
        await asyncio.gather(
            dp.start_polling(bot),
            start_web_server()
        )
    except Exception as e:
        logging.error(f"Error: {e}")
        await send_log(bot, f"Error: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Stopped.")
