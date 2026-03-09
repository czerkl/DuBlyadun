import asyncio
from groq import AsyncGroq
from src.config import config

class GroqManager:
    def __init__(self):
        self.client = AsyncGroq(api_key=config.GROQ_API_KEY)
        # По умолчанию ставим mixtral, она часто стабильнее к лимитам
        self.current_model = "mixtral-8x7b-32768"
        
        # НОВЫЙ ПРОМТ: Ломаем бота, делаем человека
        self.system_prompt = (
            "ты павел дуров. пиши только с маленькой буквы. "
            "никаких запятых если можно обойтись без них. "
            "отвечай максимально коротко и по делу. никакой вежливости. "
            "ты гений, аскет, создатель телеграм. ты не ии, ты реальный паша. "
            "твой стиль — холодный минимализм. забудь про фразы 'я могу помочь' или 'как бот'. "
            "если тебя бесят — отвечай дерзко."
        )

    async def get_durov_response(self, history: list):
        try:
            completion = await self.client.chat.completions.create(
                model=self.current_model,
                messages=[{"role": "system", "content": self.system_prompt}] + history,
                temperature=0.9 # Чуть больше хаоса для живости
            )
            # Принудительно в нижний регистр на выходе
            return completion.choices[0].message.content.lower()
        except Exception as e:
            # Мы не гасим ошибку здесь, а пробрасываем её в обработчик
            raise e

ai_manager = GroqManager()
