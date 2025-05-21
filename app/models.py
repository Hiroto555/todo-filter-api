from datetime import datetime, date
import enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    Enum,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY

from .database import Base


class StatusEnum(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(120), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(
        Enum(StatusEnum, name="status_enum", create_type=False),
        nullable=False,
        default=StatusEnum.pending,
        server_default=StatusEnum.pending.value,
    )
    due_date = Column(Date, nullable=True)
    tags = Column(ARRAY(String), nullable=False, server_default="{}")
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


