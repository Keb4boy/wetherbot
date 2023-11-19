from aiogram import Bot, Dispatcher, types
from fastapi import FastAPI, APIRouter
from aiogram.enums.parse_mode import ParseMode
from .config import API_TOKEN, WEBHOOK_URL
from .handlers import router


app = FastAPI()
webhook_router = APIRouter()
dp = Dispatcher()
dp.include_router(router=router)


@app.post("/webhook")
async def webhook(request: dict):
    update = types.Update(**request)
    await dp.feed_update(bot=bot, update=update)

async def reg_webhook():
    await bot.set_webhook(url=WEBHOOK_URL)


bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)
# bot.remove_webhook()







