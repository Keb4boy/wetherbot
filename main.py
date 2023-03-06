import requests
from geopy.geocoders import Nominatim
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from TOKEN import API_TOKEN
def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("/check"))
    return kb



# def locate(city, start, end):
#
#     geolocator = Nominatim(user_agent="weather_bot")
#
#     location = geolocator.geocode(city)
#
#     params = {"latitude":location.latitude,
#               "longitude":location.longitude,
#               "start_date":start,
#               "end_date":end,
#               "daily":["temperature_2m_max", "temperature_2m_min"],
#               "timezone":"auto"}
#     return params
#
# # def locate():
# #
# #     geolocator = Nominatim(user_agent="weather_bot")
# #
# #     location = geolocator.geocode(Moscow)
# #
# #     params = {"latitude":location.latitude,
# #               "longitude":location.longitude,
# #               "start_date":"2023-01-08",
# #               "end_date":"2023-02-08",
# #               "daily":["temperature_2m_max", "temperature_2m_min"],
# #               "timezone":"auto"}
# #     return params
#
# def weather(par):
#     weather_site = requests.get("https://archive-api.open-meteo.com/v1/archive", params = par).json()
#     return weather_site
#
#
# def date(weath):
#     date_list = []
#     for date_zone in weath["daily"]["time"]:
#         date_list.append(date_zone)
#     return date_list
#
#
# def max(weath):
#     max_list = []
#     for maximum in weath["daily"]['temperature_2m_max']:
#         max_list.append(maximum)
#     return sum(max_list) // len(max_list)
#
#
# def min(weath):
#     min_list = []
#     for minimum in weath["daily"]['temperature_2m_min']:
#         min_list.append(minimum)
#     return sum(min_list) // len(min_list)
#
# def temp(city, start, end):
#     location = weather(locate(city, start, end))
#     return f"Средняя максимальная температура в эти дни: {max(location)}\nСредняя минимальная температура в эти дни:{min(location)}"
#
# # def count():
# # print(date(location))
# # print(max(location))
# # print(min(location))


logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

class group(StatesGroup):
    city = State()
    start_date = State()
    end_date = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

    await message.reply("Я бот, который поможет тебе узнать погоду.\nДля того чтобы начать нажми /check", reply_markup=get_kb())

@dp.message_handler(commands=['check'])
async def cmd_get(message: types.Message):

    await message.reply("Для начала укажи город который тебя интересует")
    await group.city.set()

@dp.message_handler(content_types=["city"], state=group.city)
async def get_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["city"] = message.text

    await message.reply("Напишите дату, с начала которой хотите получить погоду")
    await group.next()


@dp.message_handler(content_types=["start_date"], state=group.start_date)
async def get_start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["start_date"] = message.text

    await message.reply("Напишите дату, которая является конечной")
    await group.next()


@dp.message_handler(content_types=["end_date"], state=group.end_date)
async def get_end(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["end_date"] = message.text

    await message.reply("Сейчас звгружу информацию.....")
    await state.finish()




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)






