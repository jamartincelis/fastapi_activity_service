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
    class Config:
        schema_extra = {
            "example": {
                "user": "b9e605ee-4cca-400e-99c5-ae24abca97d5",
                "project": "016fe969-4d2f-43f9-81b4-1bdcebd975e4",
                "project_name": "Nombre meta",
                "amount": 8000,
                "title": "Probando creacion de actividades",
                "message": "Probando creacion de actividades desde crear meta",
                "activity_type": "E",
                "footer": "footer",
                "rule_icon": "rule_icon"
            }
        }    

class Activity(ActivityBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "description": "Actividad",
            "example": {
                "user": "b9e605ee-4cca-400e-99c5-ae24abca97d5",
                "project": "016fe969-4d2f-43f9-81b4-1bdcebd975e4",
                "project_name": "Nombre meta",
                "rule": "null",
                "rule_name": "Probando fastapi",
                "payment": "null",
                "amount": 8000,
                "title": "Probando creacion de actividades",
                "message": "Probando creacion de actividades desde crear meta",
                "footer": "footer",
                "rule_icon": "icon",
                "activity_type": {
                "code": "E",
                "value": "Event"
                },
                "id": "fc57e25a-5612-4ee6-b66c-d63aaa536814",
                "created_at": "2022-04-03T04:12:05.793310"
            }            
        }            

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

    class Config:
        schema_extra = {
            "description": "Actividad",
            "example": {
                "rule_name": "Probando fastapi update",
                "amount": 18000,
            }            
        }            
