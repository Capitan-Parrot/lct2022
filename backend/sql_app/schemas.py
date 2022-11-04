from pydantic import BaseModel


class RegisterUserRequest(BaseModel):
    name: str
    email: str


class RegisterUser(RegisterUserRequest):
    id: int

    class Config:
        orm_mode = True


class LoginUserRequest(BaseModel):
    email: str
    password: str


class User(BaseModel):
    name: str
    email: str
    role: str
    hashed_password: str
    id: int
    is_banned: bool

    class Config:
        orm_mode = True


class RegisterUserRequest(BaseModel):
    name: str
    email: str


class Flat(BaseModel):
    address: str
    num_rooms: int
    building_segment: str
    building_num_floors: int
    building_material: str
    floor: int
    square_flat: float
    square_kitchen: float
    has_balcony: bool
    metro_distance: int
    condition: str
