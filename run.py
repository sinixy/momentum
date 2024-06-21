import asyncio


async def run():
    asyncio.create_task()

    from bot import bot, dp

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run())