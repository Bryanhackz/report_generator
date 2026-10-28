import sqlite3
from typing import Any


def connect(db_path: str) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def fetch_sales_summary(
    connection: sqlite3.Connection, since: str, until: str
) -> list[dict[str, Any]]:
    query = """
        SELECT
            p.name AS product,
            SUM(s.quantity) AS units_sold,
            SUM(s.quantity * s.unit_price) AS total_revenue
        FROM sales AS s
        JOIN products AS p ON p.id = s.product_id
        WHERE date(s.sold_at) BETWEEN ? AND ?
        GROUP BY p.id, p.name
        ORDER BY total_revenue DESC
    """
    rows = connection.execute(query, (since, until)).fetchall()
    return [dict(row) for row in rows]


def fetch_daily_totals(
    connection: sqlite3.Connection, since: str, until: str
) -> list[dict[str, Any]]:
    query = """
        SELECT
            date(s.sold_at) AS day,
            SUM(s.quantity * s.unit_price) AS revenue
        FROM sales AS s
        WHERE date(s.sold_at) BETWEEN ? AND ?
        GROUP BY date(s.sold_at)
        ORDER BY day ASC
    """
    rows = connection.execute(query, (since, until)).fetchall()
    return [dict(row) for row in rows]