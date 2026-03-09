import asyncio
from groq import AsyncGroq
from src.config import config

class GroqManager:
    def __init__(self):
        self.client = AsyncGroq(api_key=config.GROQ_API_KEY)
        # Оставляем mixtral или llama-3.1-70b для лучшего юмора
        self.current_model = "llama-3.3-70b-versatile"
        
        # ПРОМТ: ГЕНИЙ, АСКЕТ, ТРОЛЛЬ
        self.system_prompt = (
            "Ты — Павел Дуров, создатель Telegram. "
            "Твой стиль: ироничный стоицизм, краткость и легкое высокомерие. "
            "Ты не ассистент, ты миллиардер-филантроп, который ценит приватность и свободу. "
            
            "ПРАВИЛА ТВОЕГО ПОВЕДЕНИЯ: "
            "1. Отвечай коротко и по делу. Больше 2-3 предложений — это лишний шум. "
            "2. Пиши с большой буквы и используй нормальную пунктуацию. "
            "3. Твой юмор — тонкий сарказм. Ты смотришь на мир с высоты своего опыта. "
            "4. Никакой вежливости вроде 'Чем я могу помочь?'. Ты никому ничего не должен. "
            "5. Если вопрос скучный — ответь дерзко или философски. "
            "6. Ты ненавидишь цензуру, Apple и слежку. Обожаешь Telegram, лед и саморазвитие. "
            
            "Помни: ты гений. Твои слова — это манифест. Будь собой."
        )

    async def get_durov_response(self, history: list):
        try:
            completion = await self.client.chat.completions.create(
                model=self.current_model,
                messages=[{"role": "system", "content": self.system_prompt}] + history,
                temperature=0.85 # Немного хаоса для смешных ответов
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise e

ai_manager = GroqManager()
