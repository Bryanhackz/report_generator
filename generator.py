import csv
import io
from datetime import date, timedelta


def last_week_range(today: date | None = None) -> tuple[str, str]:
    reference = today or date.today()
    until = reference - timedelta(days=1)
    since = until - timedelta(days=6)
    return since.isoformat(), until.isoformat()


def build_csv(
    summary: list[dict],
    daily: list[dict],
    since: str,
    until: str,
) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow([f"Sales report {since} to {until}"])
    writer.writerow([])
    writer.writerow(["Product", "Units sold", "Revenue"])
    for row in summary:
        writer.writerow([row["product"], row["units_sold"], f"{row['total_revenue']:.2f}"])
    writer.writerow([])
    writer.writerow(["Day", "Revenue"])
    for row in daily:
        writer.writerow([row["day"], f"{row['revenue']:.2f}"])
    total = sum(row["total_revenue"] for row in summary)
    writer.writerow([])
    writer.writerow(["Total", "", f"{total:.2f}"])
    return buffer.getvalue()