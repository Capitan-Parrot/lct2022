from fastapi import APIRouter

userRouter = APIRouter(prefix="/user")


@userRouter.get("/getPrice")
async def get_price():
    from main import parser
    return parser.prices_by_district
