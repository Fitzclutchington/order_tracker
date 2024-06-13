import enum

from sqlalchemy import Boolean, Column, Enum, Integer, String

from order_tracker.database.database import Base


class RoleEnum(enum.Enum):
    ADMIN = "admin"
    SALES = "sales"
    WAREHOUSE = "warehouse"
    CLIENT = "client"
    BASIC = "basic"


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(RoleEnum), nullable=False)
