import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship

from order_tracker.database.database import Base


class StatusEnum(enum.Enum):
    SALE = "sale"
    PAYMENT = "payment"
    PRODUCTION = "production"
    DELIVERY = "delivery"
    COMPLETE = "complete"
    BLOCKED = "blocked"


class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    status = Column(Enum(StatusEnum), default=StatusEnum.SALE, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
