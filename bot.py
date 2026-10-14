import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from google import genai

# Ваши токены
TELEGRAM_BOT_TOKEN = "8877525198:AAEmfN0IQd5jskFlLgl3M5_ez_gzkdVhXdw"
GEMINI_API_KEY = "AQ.Ab8RN6KaYgoh0N5afZEMVwEAB4n3EhWhle_1-ISAcYHDolyww"

# Инициализация клиентов
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# Инструкция для бота
SYSTEM_INSTRUCTION = (
    "Ты вежливый, умный и лаконичный ИИ-помощник в групповом чате Telegram. "
    "Отвечай кратко, емко и по делу."
)

# Бот реагирует на любое текстовое сообщение, в котором есть знак вопроса "?"
@dp.message(F.text & F.text.contains("?"))
async def handle_any_question(message: Message):
    # Показываем статус "печатает..." в чате
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    try:
        # Запрос к самой мощной бесплатной модели Gemini 2.5 Pro
        response = gemini_client.models.generate_content(
            model="gemini-2.5-pro",
            contents=message.text,
            config={
                "system_instruction": SYSTEM_INSTRUCTION,
            }
        )
        
        # Отправляем ответ в виде ответа на сообщение (reply)
        await message.reply(response.text)
        
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")

async def main():
    print("Бот запущен и следит за всеми вопросами в чате (модель: gemini-2.5-pro)...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())