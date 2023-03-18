
from geopy.geocoders import Nominatim
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from TOKEN import API_TOKEN
import requests


def get_keyboard() -> ReplyKeyboardMarkup:
    # функция для создания клавиатуры
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("Moscow"), ("London"), ("Saint-Petersburg"), ("Paris"), ("Rome"))
    return kb

def get_cmdcheck() -> ReplyKeyboardMarkup:
    # функция для создания клавиатуры
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("/check"))
    return kb

def get_cmdstart() -> ReplyKeyboardMarkup:
    # функция для создания клавиатуры
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("/start"))
    return kb
def get_params(city, start, end):
    # функция для создания словаря
    dates = []
    geolocator = Nominatim(user_agent="weather_bot")

    location = geolocator.geocode(city)

    params = {"latitude": location.latitude,
              "longitude": location.longitude,
              "daily": ["temperature_2m_max", "temperature_2m_min"],
              "timezone": "auto"}

    for year in range(2013, 2023):
        params2 = {"start_date": f"{year}-{start}",
                   "end_date": f"{year}-{end}"}

        params2.update(params)

        dates.append(params2)

    return dates


def get_request(par):
    all_dates = []
    session = requests.Session()
    for param in par:
        # функция для обращения к сайту
        weather_site = session.get("https://archive-api.open-meteo.com/v1/archive", params=param).json()

        all_dates.append(weather_site)

    return all_dates
def get_max(weath):
    # функция для вычисления среднего значения максимальной температуры
    max_list = []
    for maximum in weath["daily"]['temperature_2m_max']:
        max_list.append(maximum)
    return max(max_list)


def get_min(weath):
    # функция для вычисления среднего значения минимальной температуры
    min_list = []
    for minimum in weath["daily"]['temperature_2m_min']:
        min_list.append(minimum)
    return min(min_list)

def get_average(weath):
    ave_list = []
    for ave in weath["daily"]['temperature_2m_min']:
        ave_list.append(ave)
    return sum(ave_list) // len(ave_list)

def main(city, start, end):
    minimum = []
    maximum = []
    average = []
    value = get_request(get_params(city, start, end))
    for val in value:

        minimum.append(round(get_min(val)))
        maximum.append(round(get_max(val)))
        average.append(round(get_average(val)))

    return f"Температура в эти дни от {min(minimum)} до {max(maximum)}\nСредняя температура примерно:{sum(average) // len(average)}"



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

    await message.reply("Я бот, который поможет тебе узнать погоду.\nДля того чтобы начать нажми /check", reply_markup=get_cmdcheck())

@dp.message_handler(commands=['check'])
async def cmd_get(message: types.Message):

    await message.reply("Для начала укажи город который тебя интересует", reply_markup=get_keyboard())
    await group.city.set()

@dp.message_handler(state=group.city)
async def get_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["city"] = message.text

    await message.reply("Напишите дату в формате 01-01, с начала которой хотите получить погоду")
    await group.next()


@dp.message_handler(state=group.start_date)
async def get_startdate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["start_date"] = message.text

    await message.reply("Напишите дату, которая является конечной")
    await group.next()


@dp.message_handler(state=group.end_date)
async def get_endate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["end_date"] = message.text

    await message.reply("Сейчас загружу информацию.....")
    await state.finish()
    await message.reply(main(data.get("city"), data.get('start_date'), data.get('end_date')), reply_markup=get_cmdstart())
    print(list(data.items()))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)






