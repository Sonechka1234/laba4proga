import asyncio
import logging
import os
import sys
from aiogram import F, Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
from transliterate import translit

from api import CountyAPI


load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле")

dp = Dispatcher()
api = CountyAPI()

@dp.message(CommandStart())
async def start(message: Message):
    keyboard = [
        [KeyboardButton(text='Получить случайную страну'), ]
    ]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True) 
    await message.answer(
        f"Напишите название любой страны, чтобы получить информацию о ней!",
        reply_markup=markup
    )

@dp.message(F.text != "Получить случайную страну")
async def get_country(message: Message):
    country_name = translit(message.text, 'ru')
    country_info = api.fetch_country_info(country_name)
    if country_info:
        await message.answer(
            f"🌍 **{country_info.name}**\n"
            f"🏛 Столица: {country_info.capital}\n"
            f"📍 Регион: {country_info.region}\n"
            f"📏 Площадь: {country_info.area} км²\n"
            f"👥 Население: {country_info.population}\n"
            f"🔗 [Посмотреть на карте]({country_info.maps_url})",
            disable_web_page_preview=True
        )
    else:
        await message.answer("❌ Страна не найдена. Проверьте название и попробуйте снова.")


@dp.message(F.text == "Получить случайную страну")
async def get_random_country(message: Message):
    country_info = api.fetch_random_country_info()
    if country_info:
        await message.answer(
            f"🌍 **{country_info.name}**\n"
            f"🏛 Столица: {country_info.capital}\n"
            f"📍 Регион: {country_info.region}\n"
            f"📏 Площадь: {country_info.area} км²\n"
            f"👥 Население: {country_info.population}\n"
            f"🔗 [Посмотреть на карте]({country_info.maps_url})",
            disable_web_page_preview=False
        )
    else:
        await message.answer("❌ Не удалось получить информацию о случайной стране. Попробуйте позже.")


async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())