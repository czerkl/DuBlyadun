# -*- coding: utf-8 -*-
from groq import AsyncGroq
from src.config import config

class GroqManager:
    def __init__(self):
        self.client = AsyncGroq(api_key=config.GROQ_API_KEY)
        self.current_model = "llama-3.1-8b-instant"  # Модель по умолчанию
        self.temperature = 0.8
        self.system_prompt = (
            "Ты — Павел Дуров. Твой стиль: ироничный стоицизм, краткость и уверенность. "
            "Ты создатель Telegram. Пиши с большой буквы, используй сарказм."
        )

    async def get_durov_response(self, history: list):
        try:
            completion = await self.client.chat.completions.create(
                model=self.current_model,
                messages=[{"role": "system", "content": self.system_prompt}] + history,
                temperature=self.temperature
            )
            return completion.choices[0].message.content
        except Exception as e:
            # Если модель не найдена или ошибка API, возвращаем описание ошибки
            return f"❌ Ошибка Groq ({self.current_model}): {str(e)}"

ai_manager = GroqManager()
