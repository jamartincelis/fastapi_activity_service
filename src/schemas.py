from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from pydantic_choices import choice

Activity_Type = choice(['E', 'Event', 'S', 'Saving'])

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
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
    items: List[Item] = []

    class Config:
        orm_mode = True


class ActivityBase(BaseModel):
    user: UUID
    project: UUID
    project_name: Optional[str] = None
    rule: Optional[str] = None
    rule_name: Optional[str] = None
    payment: Optional[str] = None
    amount: float
    title: str
    message: str
    footer: str
    rule_icon: str
    activity_type: Activity_Type
    

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class ActivityUpdate(BaseModel):
    user: Optional[UUID] = None
    project: Optional[UUID] = None
    project_name: Optional[str] = None
    rule: Optional[str] = None
    rule_name: Optional[str] = None
    payment: Optional[str] = None
    amount: Optional[float] = None
    title: Optional[str] = None
    message: Optional[str] = None
    footer: Optional[str] = None
    rule_icon: Optional[str] = None
    activity_type: Optional[Activity_Type] = None
