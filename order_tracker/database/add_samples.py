from datetime import datetime
from pathlib import Path

import pandas as pd

from order_tracker.database.database import SessionLocal
from order_tracker.models.orders import Orders, StatusEnum


def add_samples(samples: pd.DataFrame) -> None:
    with SessionLocal() as db:
        for _, row in samples.iterrows():
            order = Orders(
                status=StatusEnum[row["status"].upper()],  # Convert status to enum
                created_at=datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S"),
            )
            db.add(order)
        db.commit()


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    data_path = script_dir / 'sample_data' / 'test_data.csv'
    samples = pd.read_csv(data_path)
    add_samples(samples)
    print("DB upload complete")
