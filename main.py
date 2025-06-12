from aiogram.methods import DeleteWebhook
from dir_bot import create_bot, client
import asyncio


async def on_startup():
    print('Alice_bot is start!!!')


async def main():
    create_bot.dp.startup.register(on_startup)
    await create_bot.bot(DeleteWebhook(drop_pending_updates=True))
    await create_bot.dp.start_polling(create_bot.bot, polling_timeout=1)


if __name__ == '__main__':
    asyncio.run(main())
