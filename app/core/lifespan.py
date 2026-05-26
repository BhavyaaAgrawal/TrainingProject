from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Import your actual dependencies and service
from app.services.background_tasks_service import BackgroundTasksService

# 1. Create a single scheduler instance
scheduler = AsyncIOScheduler()

svc = BackgroundTasksService()

# 2. Define the wrapper function that will run periodically
# defined function in background_tasks_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 3. Attach the job to the scheduler (e.g., runs every 5 minutes)
    scheduler.add_job(
        svc.scheduled_notification_job,
        "interval",
        hours=24,
        minutes=0,
        kwargs={
            "email": "system@example.com",
            "message": "Automated periodic system notification",
            "interval": 1
        },
    )

    # 4. Start the single scheduler instance
    scheduler.start()
    print("APScheduler started successfully.")

    # write any business code logic here and as this function is wrapped inside contextmanager it will be closed by
    # calling shutdown at the last
    yield

    # 5. Shut down cleanly when the app stops
    scheduler.shutdown()
    print("APScheduler shut down successfully.")
