from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
import models, schemas
from typing import Any, Dict, Optional, Union

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def list_activities(db: Session, user_id=None, project_id = None, skip: int = 0, limit: int = 100):
    return db.query(models.Activity).filter(models.Activity.user == user_id). \
        filter(models.Activity.project == project_id).offset(skip).limit(limit).all()

def create_activity(db: Session, activity: schemas.ActivityCreate, user_id=None, project_id=None):
    obj_in_data = jsonable_encoder(activity)
    obj_in_data['user'] = user_id
    obj_in_data['project'] = project_id
    db_activity = models.Activity(**obj_in_data)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def get_activity(db: Session, user_id=None, project_id = None, activity_id = None):
    return db.query(models.Activity).filter(models.Activity.user == user_id). \
        filter(models.Activity.project == project_id). \
        filter(models.Activity.id == activity_id).first()

def update_activity(db: Session, activity: schemas.ActivityUpdate, user_id=None, project_id = None, activity_id = None):
    db_activity = get_activity(db, user_id, project_id, activity_id)
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity_data = activity.dict(exclude_unset=True)
    # Update model class variable from requested fields
    for key, value in activity_data.items():
        setattr(db_activity, key, value)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity