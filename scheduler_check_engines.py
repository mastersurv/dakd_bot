from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio
from handlers.text_handler import check_servers_and_notify


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_servers_and_notify, IntervalTrigger(minutes=2))
    scheduler.start()

    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit) as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(main())
