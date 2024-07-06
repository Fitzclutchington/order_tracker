import typing as t
from datetime import datetime
from pathlib import Path
import re

import pandas as pd
from sqlalchemy.orm import sessionmaker

from order_tracker.auth.auth import get_password_hash
from order_tracker.database.database import Base, SessionLocal, engine
from order_tracker.models.items import Items, Manufacturer
from order_tracker.models.orders import Orders, StatusEnum
from order_tracker.models.users import RoleEnum, Users


def create_test_users(test_users: list[dict]):
    with SessionLocal() as db:
        for test_user in test_users:
            user_model = Users()
            user_model.username = test_user["username"]
            user_model.email = test_user["email"]
            user_model.first_name = test_user["firstname"]
            user_model.last_name = test_user["lastname"]
            user_model.hashed_password = get_password_hash(test_user["password"])
            user_model.is_active = True
            user_model.role = RoleEnum.BASIC

            db.add(user_model)
        db.commit()


def add_orders(samples: pd.DataFrame) -> None:
    with SessionLocal() as db:
        for _, row in samples.iterrows():
            order = Orders(
                name=row["name"],
                status=StatusEnum[row["status"].upper()],  # Convert status to enum
                created_at=datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S"),
                sales_user_id=row["sales_user_id"],
            )
            db.add(order)
        db.commit()


def add_manufacturers(df: pd.DataFrame) -> None:
    manufacturers = pd.unique(df["MANUFACTURER"])
    # TODO: can this be batched?
    with SessionLocal() as db:
        for manufacturer in manufacturers:
            manufacturer_obj = Manufacturer(name=manufacturer)
            db.add(manufacturer_obj)
        db.commit()


def load_manufacturers(session: sessionmaker) -> dict[str, int]:
    manufacturers = session.query(Manufacturer).all()
    return {manufacturer.name: manufacturer.id for manufacturer in manufacturers}


def parse_dimensions(dims: str | None) -> dict[str, int]:
    if dims is None:
        return None
    dims_no_units = dims.replace("OD", "").replace('H', '').replace('W', '').replace('D', '')
    split_dims = re.split(r"[x/]", dims_no_units)
    dims_dict = {
        "height": int(split_dims[0]),
        "width": int(split_dims[1]),
        "depth": int(split_dims[2]),
    }
    if len(split_dims) == 4:
        dims_dict["overall_depth"] = int(split_dims[3])
    
    return dims_dict


def parse_price(price: str) -> dict[str, t.Any]:
    pass


def add_items(df: pd.DataFrame) -> None:
    with SessionLocal() as db:
        manufacturers = load_manufacturers(db)
        for _, row in df.iterrows():

            manufacturer_name = row["MANUFACTURER"]
            manufacturer_id = manufacturers.get(manufacturer_name)

            if manufacturer_id is None:
                manufacturer_id = 99999

            inside_dims = parse_dimensions(row["INSIDE DIMENSIONS"])
            outside_dims = parse_dimensions(row["OUTSIDE DIMENSIONS"])
            parsed_price = parse_price(row["price"])
            # TODO: function to parse dimensions
            # TODO: function to parse price
            item = Items(
                manufacturer_id=manufacturer_id,
                model_name=row["MODEL"],
                series=row["SERIES"],
                url=row["URL"],
                security_level=row["SECURITY LEVEL"],
                height_inside=inside_dims.get("height"),
                height_outside=outside_dims.get("height"),
                width_inside=inside_dims.get("width"),
                width_outside=outside_dims.get("width"),
                depth_inside=inside_dims.get("depth"),
                depth_outside=outside_dims.get("depth"),
                overall_depth=outside_dims.get("overal_depth"),
                capacity=float(row["CAPACITY"].split()[0]) if row["CAPACITY"] else None,
                fire_protection=row["FIRE PROTECTION"],
                weight=int(row["WEIGHT"]) if row["WEIGHT"] else None,
                price=parsed_price["price"],
                currency=parsed_price["currency"],
                swing=row["SWING"],
            )
            db.add(item)
        db.commit


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    script_dir = Path(__file__).parent
    data_path = script_dir / "sample_data"
    order_samples = pd.read_csv(data_path / "test_data.csv")
    items_samples = pd.read_csv(data_path / "items.csv")

    test_users = [
        {
            "username": "test1",
            "email": "test1@gmail.com",
            "firstname": "test1",
            "lastname": "test1",
            "password": "password",
        },
        {
            "username": "test2",
            "email": "test2@gmail.com",
            "firstname": "test2",
            "lastname": "test2",
            "password": "password",
        },
    ]
    create_test_users(test_users)
    add_orders(order_samples)
    add_manufacturers(items_samples)
    add_items(items_samples)
    print("DB upload complete")
