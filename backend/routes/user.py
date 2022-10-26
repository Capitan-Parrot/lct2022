from datetime import datetime

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from backend.dependencies import get_flats_from_excel_file
from backend.sql_app import schemas
from backend.sql_app.crud import create_user, create_register_request
from backend.sql_app.database import get_db

userRouter = APIRouter(prefix="/user")


@userRouter.get("/getPrice")
async def get_price():
    from backend.main import parser
    return parser.prices_by_district


@userRouter.post("/register")
async def register(register_request: schemas.RegisterRequestCreate, db: Session = Depends(get_db)):
    request = create_register_request(db, register_request)
    return 'ok'


@userRouter.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    flats = await get_flats_from_excel_file(file)
    return flats
