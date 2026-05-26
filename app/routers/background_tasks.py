from fastapi import APIRouter, BackgroundTasks, Depends

from app.services.background_tasks_service import BackgroundTasksService

router = APIRouter(prefix="/background-tasks", tags=["BackgroundTasks"])

@router.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks,
                            svc:BackgroundTasksService=Depends(BackgroundTasksService)):
    # Use keyword arguments to avoid positional mismatches and to be resilient if
    # the service signature changes.
    background_tasks.add_task(svc.write_notification, email=email, message="some notification")
    return {"message": "Notification sent in the background"}
