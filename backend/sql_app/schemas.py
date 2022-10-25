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


class RegisterUser(BaseModel):
    id: int


class UserBase(BaseModel):
    name: str
    surname: str
    patronymic: str
    email: str
    role: str
    hashed_password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_banned: bool

    class Config:
        orm_mode = True