from fastapi import APIRouter
from starlette.background import BackgroundTasks

from .admin import adminRouter
from .user import userRouter

router = APIRouter(prefix="/api")

router.include_router(adminRouter)
router.include_router(userRouter)

