from pydantic import BaseModel
from datetime import date, time


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: str = "pending"
    subject: str
    date: date
    time: time


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Task] = []

    class Config:
        orm_mode = True
