from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from ..sql_app import crud, schemas
from ..sql_app.database import get_db
from backend.MailService import send_email


adminRouter = APIRouter(prefix="/admin",
                        tags=["admin"])


@adminRouter.get("/getAllUsers", response_model=list[schemas.User])
async def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@adminRouter.get("/getAllRegisterRequests", response_model=list[schemas.RegisterUserRequest])
async def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_register_requests(db, skip=skip, limit=limit)
    return users


@adminRouter.post("/createUser/{register_id}", response_model=schemas.User)
async def register(register_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = crud.get_register_request(db, register_id)
    user, user_password = crud.create_user(db, user)
    send_email(background_tasks, 'Ваши данные для входа',
               user.email, {'title': 'Данные для входа', 'name': user.name, 'password': user_password})
    return user, user_password

