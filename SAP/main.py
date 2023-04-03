from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
token = '6208415025:AAG-9HSM5_rSZEBoy8o7RS8LeFgJSMwoWE8'

ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('❤️', callback_data='like'), InlineKeyboardButton('😡', callback_data='dislike')],
])

bot = Bot(token=token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await bot.send_photo(chat_id=message.from_user.id,
                         photo='https://cdn.forbes.ru/files/1082x683/photo_galleries/1920-02_tcm-3173-1834873.jpg__1582289253__55999.webp',
                         caption='Нравится ли тебе фотография?',
                         reply_markup=ikb)

# @dp.callback_query_handler()





if __name__ ==  '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)