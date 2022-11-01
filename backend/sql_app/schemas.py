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
    num_rooms: str
    building_segment: str
    building_num_floors: str
    building_material: str
    floor: str
    building_segment: str
    building_num_floors: str
    building_material: str
    square_flat: str
    square_kitchen: str
    has_balcony: bool
    metro_distance: int
