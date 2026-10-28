import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path


SCHEMA_PATH = Path(__file__).with_name("schema.sql")
DEMO_PRODUCTS = [
    ("Wireless mouse", 24.90),
    ("USB-C cable", 12.50),
    ("Mechanical keyboard", 89.00),
    ("Monitor stand", 45.00),
    ("Webcam 1080p", 59.90),
]


def seed(db_path: str) -> None:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    connection = sqlite3.connect(db_path)
    try:
        connection.executescript(schema)
        connection.executemany(
            "INSERT OR IGNORE INTO products (name, unit_price) VALUES (?, ?)",
            DEMO_PRODUCTS,
        )
        product_rows = connection.execute("SELECT id, unit_price FROM products").fetchall()
        today = date.today()
        sales: list[tuple[int, int, float, str]] = []
        for offset in range(14):
            day = (today - timedelta(days=offset)).isoformat()
            for _ in range(random.randint(1, 4)):
                product_id, unit_price = random.choice(product_rows)
                sales.append(
                    (product_id, random.randint(1, 5), unit_price, day)
                )
        connection.executemany(
            "INSERT INTO sales (product_id, quantity, unit_price, sold_at) VALUES (?, ?, ?, ?)",
            sales,
        )
        connection.commit()
        print(f"Seeded {len(sales)} sales over {len(DEMO_PRODUCTS)} products into {db_path}")
    finally:
        connection.close()


if __name__ == "__main__":
    seed("sales.db")