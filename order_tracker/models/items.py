from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    func,
    Float
)

from order_tracker.database.database import Base


class Manufacturer(Base):
    __tablename__ = "manufacturers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class Items(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), nullable=False)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"))
    model_name = Column(String)
    series = Column(String)
    url = Column(String)
    security_level = Column(String)
    height_inside = Column(Integer)
    height_outside = Column(Integer)
    width_inside = Column(Integer)
    width_outside = Column(Integer)
    depth_inside = Column(Integer)
    depth_outside = Column(Integer)
    overall_depth = Column(Integer)
    capacity = Column(Float)
    capacity_unit = Column(String)
    fire_protection = Column(String)
    weight = Column(Integer)
    weight_unit = Column(String)
    price = Column(Float)
    currency = Column(String)
    swing = Column(String)
