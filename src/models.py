from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

from sqlalchemy.types import TypeDecorator, CHAR, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database import Base
from datetime import datetime
from alembic import op
from sqlalchemy_utils.types.choice import ChoiceType


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class Activity(Base):

    __tablename__ = "activities"

    id = Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    user = Column(GUID(), index=True, nullable=False)
    project = Column(GUID(), index=True, nullable=False)
    rule = Column(GUID(), index=True, nullable=True)
    payment = Column(GUID(), index=True, nullable=True)
    project_name = Column(String(60), nullable=True, default=None)
    rule_name = Column(String(60), nullable=True, default=None)
    amount = Column(Float(12,2), nullable=True, default=None)
    title = Column(String(200), nullable=True, default=None)
    message = Column(String(300), nullable=True, default=None)
    footer = Column(String(200), nullable=True, default=None)
    rule_icon = Column(String(60), nullable=True, default=None)
    created_at = Column(DateTime, default=datetime.now)

    # indica el tipo de actividad

    ACTIVITY_TYPE_CHOICES = [
        ('E', 'Event'),
        ('S', 'Saving'),
    ]    

    activity_type = Column(
        ChoiceType(ACTIVITY_TYPE_CHOICES), nullable=True, default=None,
    )