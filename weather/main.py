from aiogram import Bot, Dispatcher, types
from fastapi import FastAPI, APIRouter
from aiogram.enums.parse_mode import ParseMode
from .config import API_TOKEN, WEBHOOK_URL
from .handlers import router
import logging
from aiogram.types import webhook_info

logger = logging.getLogger(__name__)

app = FastAPI()
webhook_router = APIRouter()
dp = Dispatcher()
dp.include_router(router=router)
bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)

@app.post("/webhook")
async def webhook(request: dict):
    update = types.Update(**request)
    logger.debug(update)
    await dp.feed_update(bot=bot, update=update)

async def reg_webhook():
    await bot.set_webhook(url=WEBHOOK_URL)
    webhook_info = await bot.get_webhook_info()
    logger.info(f"""Webhook info: {webhook_info}""")



# bot.remove_webhook()

@app.on_event("startup")
async def on_startup():
    await reg_webhook()







