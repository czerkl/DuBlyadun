import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TG_TOKEN = os.getenv("TG_TOKEN")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
    PORT = int(os.getenv("PORT", 8080))
    
    _log_id = os.getenv("LOG_CHAT_ID")
    LOG_CHAT_ID = int(_log_id) if _log_id else None

config = Config()

# Жёсткая проверка: теперь корректно обрабатывает ADMIN_ID=0
required_vars = {
    "TG_TOKEN": config.TG_TOKEN,
    "GROQ_API_KEY": config.GROQ_API_KEY,
    "SUPABASE_URL": config.SUPABASE_URL,
    "SUPABASE_KEY": config.SUPABASE_KEY
}

for name, val in required_vars.items():
    if not val:
        raise ValueError(f"Критическая ошибка: Переменная {name} отсутствует в .env!")

if config.ADMIN_ID == 0:
    print("⚠️ Внимание: ADMIN_ID не установлен, доступ к панели управления ограничен.")
