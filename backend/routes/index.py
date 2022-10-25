from fastapi import APIRouter
from backend.routes.admin import adminRouter
from backend.routes.user import userRouter

router = APIRouter(prefix="/api")
router.include_router(adminRouter)
router.include_router(userRouter)

@router.get("/")
async def root():
    return {"message": "Hello Api"}
