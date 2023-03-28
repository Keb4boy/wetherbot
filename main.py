import aiohttp
from geopy.geocoders import Nominatim
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.environ.get("API_TOKEN")


def get_keyboard() -> ReplyKeyboardMarkup:
    """Create keyboard with cities"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("Moscow"), ("London"), ("Saint-Petersburg"), ("Paris"), ("Rome"))
    return kb

def get_cmdcheck() -> ReplyKeyboardMarkup:
    """Create keyboard for command /check"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("/check"))
    return kb

def get_cmdstart() -> ReplyKeyboardMarkup:
    """Create keyboard for command /start"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("/start"))
    return kb
def get_params(city, start, end):
    """Generating params for weather API"""
    dates = []
    geolocator = Nominatim(user_agent="weather_bot")

    location = geolocator.geocode(city)

    params = {"latitude": location.latitude,
              "longitude": location.longitude,
              "daily": ["temperature_2m_max", "temperature_2m_min"],
              "timezone": "auto"}

    for year in range(2020, 2023):
        params2 = {"start_date": f"{year}-{start}",
                   "end_date": f"{year}-{end}"}

        params2.update(params)

        dates.append(params2)

    return dates

async def fetch_result(session, params):
    """Creates json file with weather values"""
    async with session.get('https://archive-api.open-meteo.com/v1/archive', params=params) as result:
        return await result.json()
async def get_request(all_params):
    """Creates asynchronous requests"""
    async with aiohttp.ClientSession() as session:
        requests = [fetch_result(session, params) for params in all_params]
        result = await asyncio.gather(*requests, return_exceptions=False)

        return result


def get_max(weath):
    """Sorts json file and return max value"""
    max_list = []
    for maximum in weath["daily"]['temperature_2m_max']:
        max_list.append(maximum)
    return max(max_list)


def get_min(weath):
    """Sorts json file and return min value"""
    min_list = []
    for minimum in weath["daily"]['temperature_2m_min']:
        min_list.append(minimum)
    return min(min_list)

def get_average(weath):
    """Sorts json file and return average value"""
    ave_list = []
    for ave in weath["daily"]['temperature_2m_min']:
        ave_list.append(ave)
    return sum(ave_list) // len(ave_list)

async def main(city, start, end):
        """Makes lists with all values and sorts it"""
        minimum = []
        maximum = []
        average = []
        value = await get_request(get_params(city, start, end))
        for val in value:

            minimum.append(round(get_min(val)))
            maximum.append(round(get_max(val)))
            average.append(round(get_average(val)))

        return f"Температура в эти дни от {min(minimum)} до {max(maximum)}\nСредняя температура примерно:{sum(average) // len(average)}"



logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

class Group(StatesGroup):
    city = State()
    start_date = State()
    end_date = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

    await message.reply("Я бот, который поможет тебе узнать погоду.\nДля того чтобы начать нажми /check", reply_markup=get_cmdcheck())

@dp.message_handler(commands=['check'])
async def cmd_get(message: types.Message):

    await message.reply("Для начала укажи город который тебя интересует", reply_markup=get_keyboard())
    await Group.city.set()

@dp.message_handler(state=Group.city)
async def get_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["city"] = message.text

    await message.reply("Напишите дату в формате 01-01 (месяц-день), с начала которой хотите получить погоду")
    await Group.next()


@dp.message_handler(state=Group.start_date)
async def get_startdate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["start_date"] = message.text

    await message.reply("Напишите дату, которая является конечной")
    await Group.next()


@dp.message_handler(state=Group.end_date)
async def get_endate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["end_date"] = message.text

    await message.reply("Сейчас загружу информацию.....")
    await state.finish()
    await message.reply(await main(data.get("city"), data.get('start_date'), data.get('end_date')))



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)






