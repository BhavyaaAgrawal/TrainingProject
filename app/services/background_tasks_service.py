from apscheduler.triggers import interval

from app.core.logger import setup_logger

logger = setup_logger()

class BackgroundTasksService:
    def __init__(self):
        pass

    async def scheduled_notification_job(self, email: str, message: str = "", interval: int = 1):
        """Scheduler entrypoint (no request context)."""
        await self.write_notification(email=email, message=message, interval=interval)

    async def write_notification(self, email: str | None = None, message: str = "", interval: int = 1):
        # Background tasks run after the response is returned; if wiring is wrong,
        # we don't want to crash the request cycle.
        if not email:
            logger.error("write_notification called without email")
            return
        logger.info('Scheduled task running in {interval} minutes'.format(interval=interval))
        logger.info(f"Writing notification to email {email}")