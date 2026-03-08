import asyncio
from groq import AsyncGroq
from src.config import config

class GroqManager:
    def __init__(self):
        self.client = AsyncGroq(api_key=config.GROQ_API_KEY)
        self.system_prompt = (
            "Ты — Павел Дуров. Ты аскет, гений, создатель Telegram. "
            "Твой язык остр, мысли глубоки, ответы коротки. "
            "Никакой вежливости ради вежливости. Только суть."
        )

    async def get_durov_response(self, history: list):
        try:
            completion = await self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "system", "content": self.system_prompt}] + history,
                temperature=0.8
            )
            return completion.choices[0].message.content
        except Exception as e:
            err_str = str(e).lower()
            # ПУНКТ №5: Если Groq перегружен (Rate Limit)
            if "rate_limit" in err_str or "429" in err_str:
                return "Слишком много запросов. Даже мои серверы требуют тишины. Подожди минуту."
            
            # Если любая другая ошибка
            return "Цифровой шум мешает связи. Повтори запрос позже, когда архитектура стабилизируется."

ai_manager = GroqManager()