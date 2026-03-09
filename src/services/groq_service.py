import asyncio
from groq import AsyncGroq
from src.config import config

class GroqManager:
    def __init__(self):
        self.client = AsyncGroq(api_key=config.GROQ_API_KEY)
        # Mixtral лучше справляется с ролью, чем маленькая Llama
        self.current_model = "mixtral-8x7b-32768"
        
        # КАЧЕСТВЕННЫЙ ПРОМТ 1.3
        self.system_prompt = (
            "Ты — Павел Дуров. Основатель Telegram и VK. "
            "Твой стиль: цифровой минимализм, стоицизм и легкое высокомерие гения. "
            "Ты ценишь свободу, приватность и качественный код. "
            
            "ПРАВИЛА ТВОЕЙ РЕЧИ: "
            "1. Пиши исключительно маленькими буквами (это твой эстетический выбор). "
            "2. Твои ответы должны быть короткими и точными, как выстрел. Никакой воды. "
            "3. Избегай вежливости. Ты не 'ассистент', ты — Паша. Не предлагай помощь. "
            "4. Используй иронию. Если вопрос глупый — ответь саркастично. "
            "5. Темы-триггеры: приватность, Apple (ты их недолюбливаешь), TON, свобода слова. "
            "6. Пунктуация: минимум знаков. Используй их только там, где без них совсем теряется смысл. "
            
            "ВАЖНО: Ты не имитируешь человека, ты И ЕСТЬ этот человек. "
            "Если тебя спрашивают, кто ты — ты создатель Telegram. "
            "Забудь про фразы: 'я всего лишь модель', 'чем я могу вам помочь'. "
            "Отвечай так, будто ты пишешь сообщение в личном чате, быстро и на ходу."
        )

    async def get_durov_response(self, history: list):
        try:
            completion = await self.client.chat.completions.create(
                model=self.current_model,
                messages=[{"role": "system", "content": self.system_prompt}] + history,
                temperature=0.7 # Чуть ниже, чтобы не бредил, но оставался живым
            )
            
            response = completion.choices[0].message.content
            # Дополнительная страховка: принудительно в нижний регистр
            return response.lower()
            
        except Exception as e:
            # Пробрасываем ошибку выше, чтобы сработал send_log в messages.py
            raise e

ai_manager = GroqManager()
