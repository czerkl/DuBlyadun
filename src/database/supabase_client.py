from supabase import create_client, Client
from src.config import config

class SupabaseManager:
    def __init__(self):
        self.client: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
        self.table_name = "chat_memory"

    def save_message(self, chat_id: int, role: str, content: str):
        data = {
            "chat_id": chat_id,
            "role": role,
            "content": content
        }
        # Убрали try-except, чтобы ошибка летела в messages.py и далее в логи
        return self.client.table(self.table_name).insert(data).execute()

    def get_history(self, chat_id: int, limit: int = 15):
        response = self.client.table(self.table_name) \
            .select("role", "content") \
            .eq("chat_id", chat_id) \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        
        return [{"role": item["role"], "content": item["content"]} for item in reversed(response.data)]

db = SupabaseManager()
