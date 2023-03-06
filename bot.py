import logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '6040815865:AAH0JV5JAd3vxXU48U0pPGC-2R9GC-aVhu4'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["pidor"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Вы все пидоры")

@dp.message_handler(commands=["dima"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("@ddssvvvujnnj хуесос")

@dp.message_handler(commands=["vadik"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("вадик красавчик")

@dp.message_handler(commands=["kukold"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("@ddssvvvujnnj куколд")

@dp.message_handler(commands=["алкаш"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Иди проспить @Renatq7")

# @dp.message_handler()
# async def weath(message: types.Message):
#     # old style:
#     # await bot.send_message(message.chat.id, message.text)
#
#     await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)