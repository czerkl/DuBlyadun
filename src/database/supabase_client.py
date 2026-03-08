from supabase import create_client, Client
from src.config import config

class SupabaseManager:
    def __init__(self):
        # Инициализируем соединение с Supabase
        self.client: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
        self.table_name = "chat_memory"

    def save_message(self, chat_id: int, role: str, content: str):
        """
        Сохраняет сообщение в таблицу.
        role: 'user' (от пользователя) или 'assistant' (от Дурова)
        """
        try:
            data = {
                "chat_id": chat_id,
                "role": role,
                "content": content
            }
            # Используем .execute() - это актуальный метод в текущей версии библиотеки
            return self.client.table(self.table_name).insert(data).execute()
        except Exception as e:
            print(f"Ошибка при сохранении в БД: {e}")

    def get_history(self, chat_id: int, limit: int = 15):
        """
        Достает последние сообщения, чтобы Дуров был в контексте.
        """
        try:
            response = self.client.table(self.table_name) \
                .select("role", "content") \
                .eq("chat_id", chat_id) \
                .order("created_at", desc=True) \
                .limit(limit) \
                .execute()
            
            # Важно: сообщения приходят в обратном порядке (от новых к старым)
            # Для ИИ нам нужно перевернуть их, чтобы шел нормальный диалог
            history = [{"role": item["role"], "content": item["content"]} for item in reversed(response.data)]
            return history
        except Exception as e:
            print(f"Ошибка при получении истории: {e}")
            return []

# Создаем экземпляр базы данных для использования в других файлах
db = SupabaseManager()