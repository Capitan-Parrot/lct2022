from pydantic import BaseModel


class RegisterRequestBase(BaseModel):
    name: str
    surname: str
    patronymic: str
    email: str


class RegisterRequestCreate(RegisterRequestBase):
    pass


class RegisterRequest(RegisterRequestBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    surname: str
    patronymic: str
    email: str
    role: str
    hashed_password: str


class User(UserBase):
    id: int
    is_banned: bool

    class Config:
        orm_mode = True

class UserIn(BaseModel):
    id: int


class UserOut(BaseModel):
    user: User
    password: str


class UserCreate(UserBase):
    pass


