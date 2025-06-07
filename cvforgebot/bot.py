import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from cvforgebot.config import BOT_TOKEN, REDIS_DSN
from cvforgebot.handlers import start, form, generate

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
async def main():
    # Initialize Redis storage
    storage = RedisStorage.from_url(REDIS_DSN)
    
    # Initialize bot and dispatcher
    bot = Bot(token="7341551375:AAFzI-4i2xplMLRckSfjgKnvZNch6fnrW6E")
    dp = Dispatcher(storage=storage)
    
    # Register handlers
    dp.include_router(start.router)
    dp.include_router(form.router)
    dp.include_router(generate.router)
    
    # Start polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main()) 