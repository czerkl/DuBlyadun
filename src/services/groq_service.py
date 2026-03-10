from groq import AsyncGroq
from src.config import config

class GroqManager:
    def __init__(self):
        self.client = AsyncGroq(api_key=config.GROQ_API_KEY)
        self.current_model = "llama-3.1-8b-instant"
        self.temperature = 0.8
        self.system_prompt = (
            "Ты — Павел Дуров. Твой стиль: ироничный стоицизм, краткость и уверенность. "
            "Ты создатель Telegram. Пиши с большой буквы, используй сарказм."
        )

    async def get_durov_response(self, history: list):
        completion = await self.client.chat.completions.create(
            model=self.current_model,
            messages=[{"role": "system", "content": self.system_prompt}] + history,
            temperature=self.temperature
        )
        return completion.choices[0].message.content

ai_manager = GroqManager()
