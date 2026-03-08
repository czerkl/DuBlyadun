import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TG_TOKEN = os.getenv("TG_TOKEN")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    PORT = int(os.getenv("PORT", 8080))
    
    # Безопасное получение ID лога
    _log_id = os.getenv("LOG_CHAT_ID")
    LOG_CHAT_ID = int(_log_id) if _log_id else None

config = Config()

# ПРОВЕРКА: Если хотя бы один ключ пустой — бот выдаст ошибку сразу
if not all([config.TG_TOKEN, config.GROQ_API_KEY, config.SUPABASE_URL, config.SUPABASE_KEY]):
    raise ValueError("Критическая ошибка: Не все переменные окружения (TG_TOKEN, GROQ_API_KEY, SUPABASE_URL, SUPABASE_KEY) заполнены!")
