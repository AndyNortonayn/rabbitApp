import logging
from gc import callbacks

import urllib3
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.token import TokenValidationError
import asyncio
import requests




logging.basicConfig(level=logging.INFO)

try:
    bot = Bot(token=API_TOKEN)
except TokenValidationError:
    logging.error("Invalid Bot Token!")

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def get_photo(user_id: int):
    user_photos = await bot.get_user_profile_photos(user_id)
    if user_photos.total_count > 0:
        file_id = user_photos.photos[0][0].file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        photo_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_path}"
        return photo_url
    return None

async def check_command_start(message_text: str):
    print(message_text)
    if '/start' in message_text:
        start = message_text.replace('/start ', '')

        if start == '/start':
            return None

        return start
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
@dp.callback_query(F.data == "ref")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(f'Ваша реферальная ссылка:\nhttps://t.me/Grani_trening_bot?start={callback.message.chat.id}')
@dp.message()
async def start(message: types.Message):
    referral_id = await check_command_start(message.text)
    avatar_url = await get_photo(message.from_user.id)

    data = {
        'user_id': message.from_user.id,
        'nick_name': message.from_user.username,
        'avatar': avatar_url,
        'referal_id': referral_id,
    }

    logging.info(f"Отправка данных на сервер: {data}")

    url = 'https://rabbit-test.ru/startButton/'

    try:
        response = requests.post(url, json=data, verify=False)
        response.raise_for_status()  # Проверка на успешный статус
        logging.info(f"Response status code: {response.status_code}")
        logging.info(f"Response data: {response.json()}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Запрос не удался: {e}")

    web_app = WebAppInfo(url="https://rabbitapp-master-main2.vercel.app/")
    web_app_button = InlineKeyboardButton(
        text="Open Web App",
        web_app=web_app
    )
    ref =InlineKeyboardButton(
        text = 'Реф ссылка',
        callback_data = 'ref'
    )

    await bot.delete_webhook()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[web_app_button],[ref]])
    await message.answer("Click the button to open the Web App", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
