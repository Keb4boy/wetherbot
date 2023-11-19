from aiogram import types, Router
from .func import get_values
from .kb import get_cmdcheck#, get_keyboard
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


router = Router()

class Group(StatesGroup):
    city = State()
    start_date = State()
    end_date = State()



@router.message(Command("start"))
async def send_welcome(msg: Message):

    await msg.answer("Я бот, который поможет тебе узнать погоду.\nДля того чтобы начать нажми /check", reply_markup=get_cmdcheck())

# @router.message(Command("check"))
# async def cmd_get(msg: Message):

#     await msg.answer("Для начала укажи город который тебя интересует", reply_markup=get_keyboard())
#     await Group.city.set()

# @router.message(state=Group.city)
# async def get_city(msg: Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["city"] = msg.text

#     await msg.reply("Напишите дату в формате 01-01 (месяц-день), с начала которой хотите получить погоду")
#     await Group.next()


# @router.message(state=Group.start_date)
# async def get_startdate(msg: Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["start_date"] = msg.text

#     await msg.reply("Напишите дату, которая является конечной")
#     await Group.next()


# @router.message(state=Group.end_date)
# async def get_endate(msg: Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["end_date"] = msg.text

#     await msg.reply("Сейчас загружу информацию.....")
#     await state.finish()
#     values = await get_values(data.get("city"), data.get('start_date'), data.get('end_date'))
#     await msg.reply(values)