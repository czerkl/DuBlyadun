import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TG_TOKEN = os.getenv("TG_TOKEN")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    # Добавляем ID админа (превращаем в int для сравнения)
    ADMIN_ID = int(os.getenv("ADMIN_ID", 0)) 
    PORT = int(os.getenv("PORT", 8080))
    
    _log_id = os.getenv("LOG_CHAT_ID")
    LOG_CHAT_ID = int(_log_id) if _log_id else None

config = Config()

if not all([config.TG_TOKEN, config.GROQ_API_KEY, config.SUPABASE_URL, config.SUPABASE_KEY, config.ADMIN_ID]):
    raise ValueError("Критическая ошибка: В переменных окружения не хватает данных (проверь ключи Supabase и ADMIN_ID)!")