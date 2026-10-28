import argparse
import logging
import sys
from contextlib import closing
from datetime import date

from config import load_config
from db import connect, fetch_daily_totals, fetch_sales_summary
from generator import build_csv, last_week_range
from mailer import send_report


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("report")


def _parse_date(value: str) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid date: {value}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate and email the weekly sales report."
    )
    parser.add_argument("--since", type=_parse_date, help="Start date (YYYY-MM-DD).")
    parser.add_argument("--until", type=_parse_date, help="End date (YYYY-MM-DD).")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the CSV to stdout, do not send email.",
    )
    parser.add_argument(
        "--output",
        help="Write the CSV to this path instead of emailing.",
    )
    args = parser.parse_args(argv)

    if bool(args.since) != bool(args.until):
        parser.error("--since and --until must be provided together")

    config = load_config()
    if args.since and args.until:
        since, until = args.since, args.until
    else:
        since, until = last_week_range()

    try:
        with closing(connect(config.db_path)) as connection:
            summary = fetch_sales_summary(connection, since, until)
            daily = fetch_daily_totals(connection, since, until)
    except Exception as exc:
        log.error("Database error: %s", exc)
        return 1

    if not summary:
        log.warning("No sales between %s and %s, nothing to send", since, until)
        return 0

    csv_content = build_csv(summary, daily, since, until)
    filename = f"sales_{since}_{until}.csv"

    if args.output:
        with open(args.output, "w", encoding="utf-8", newline="") as handle:
            handle.write(csv_content)
        log.info("Report written to %s", args.output)
        return 0

    if args.dry_run:
        log.info("Dry run: %d products, %d days", len(summary), len(daily))
        sys.stdout.write(csv_content)
        return 0

    subject = f"Sales report {since} to {until}"
    body = (
        f"Weekly sales report from {since} to {until}.\n\n"
        f"Products sold: {len(summary)}\n"
        f"Days with activity: {len(daily)}\n"
    )
    try:
        send_report(config, subject, body, csv_content, filename)
    except Exception as exc:
        log.error("Email error: %s", exc)
        return 1
    log.info("Report sent to %s", config.report_recipient)
    return 0


if __name__ == "__main__":
    sys.exit(main())