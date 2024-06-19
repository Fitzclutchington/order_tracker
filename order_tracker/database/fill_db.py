from datetime import datetime
from pathlib import Path

import pandas as pd

from order_tracker.auth.auth import get_password_hash
from order_tracker.database.database import Base, SessionLocal, engine
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


def add_samples(samples: pd.DataFrame) -> None:
    with SessionLocal() as db:
        for _, row in samples.iterrows():
            order = Orders(
                name=row["name"],
                status=StatusEnum[row["status"].upper()],  # Convert status to enum
                created_at=datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S"),
            )
            db.add(order)
        db.commit()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    script_dir = Path(__file__).parent
    data_path = script_dir / "sample_data" / "test_data.csv"
    samples = pd.read_csv(data_path)

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
    add_samples(samples)
    print("DB upload complete")
