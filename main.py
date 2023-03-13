import requests
from geopy.geocoders import Nominatim
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from TOKEN import API_TOKEN


def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("Moscow"), ("London"), ("Saint-Petersburg"), ("Paris"), ("Rome"))
    return kb



def get_params(city, start, end, year):

    geolocator = Nominatim(user_agent="weather_bot")

    location = geolocator.geocode(city)

    params = {"latitude":location.latitude,
              "longitude":location.longitude,
              "start_date":f"{year}-{start}",
              "end_date":f"{year}-{end}",
              "daily":["temperature_2m_max", "temperature_2m_min"],
              "timezone":"auto"}
    return params


def get_request(par):
    weather_site = requests.get("https://archive-api.open-meteo.com/v1/archive", params = par).json()
    return weather_site


def date(weath):
    date_list = []
    for date_zone in weath["daily"]["time"]:
        date_list.append(date_zone)
    return date_list


def max(weath):
    max_list = []
    for maximum in weath["daily"]['temperature_2m_max']:
        max_list.append(maximum)
    return sum(max_list) / len(max_list)


def min(weath):
    min_list = []
    for minimum in weath["daily"]['temperature_2m_min']:
        min_list.append(minimum)
    return sum(min_list) / len(min_list)

def main(city, start, end):
    for year in range(2000, 2021):
        value = get_request(get_params(city, start, end, year))
        print(value)
    return f"Средняя максимальная температура в эти дни: {max(value)}\nСредняя минимальная температура в эти дни:{min(value)}"



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

    await message.reply("Я бот, который поможет тебе узнать погоду.\nДля того чтобы начать нажми /check")

@dp.message_handler(commands=['check'])
async def cmd_get(message: types.Message):

    await message.reply("Для начала укажи город который тебя интересует", reply_markup=get_kb())
    await group.city.set()

@dp.message_handler(state=group.city)
async def get_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["city"] = message.text

    await message.reply("Напишите дату в формате 01-01, с начала которой хотите получить погоду")
    await group.next()


@dp.message_handler(state=group.start_date)
async def get_start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["start_date"] = message.text

    await message.reply("Напишите дату, которая является конечной")
    await group.next()


@dp.message_handler(state=group.end_date)
async def get_end(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["end_date"] = message.text

    await message.reply("Сейчас загружу информацию.....")
    await state.finish()
    await message.reply(main(data.get("city"), data.get('start_date'), data.get('end_date')))
    print(list(data.items()))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)






