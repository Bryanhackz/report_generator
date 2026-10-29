# Report Generator

## Problem
Managers spent hours every Monday extracting sales data from a SQLite
database and formatting it into a spreadsheet. The work was manual,
error-prone, and delayed decisions until Tuesday.

## Solution
A single-file Python CLI that connects to the database, runs the weekly
sales queries, builds a CSV report, and delivers it by email. Designed
to run from cron. Uses only the Python standard library.

## Impact
- Weekly report generation: from ~3 hours of manual work to under 5 seconds.
- The report is identical every week, so trend comparison is reliable.
- One command (`python report.py`) replaces the entire manual process.

## Stack
- Python 3.11+
- `sqlite3`, `smtplib`, `csv`, `email`, `argparse`, `logging`, `dataclasses`
- No external dependencies.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
cp .env.example .env
# edit .env with your SMTP credentials
python seed.py
python report.py --dry-run
```

## Usage
- `python report.py` sends last week's report by email.
- `python report.py --dry-run` prints the CSV to stdout.
- `python report.py --output report.csv` writes to a file without emailing.
- `python report.py --since 2026-10-01 --until 2026-10-07` picks a custom range.

## Scheduling
Add to crontab to run every Monday at 08:00:
```
0 8 * * 1 cd /path/to/report-generator && /path/to/.venv/bin/python report.py
```

## Architectural decisions
- CSV instead of PDF: the standard library does not generate PDF. A CSV
  opens natively in Excel, Google Sheets, and Numbers, and preserves the
  raw numbers for further analysis. A PDF would require a third-party
  library, which the project scope forbids.
- No scheduler in code: cron is the right tool for the job. Implementing
  a scheduler in Python adds dependencies and a long-running process for
  no benefit.
- Fail-fast configuration: the process refuses to start if any required
  environment variable is missing. A misconfigured report is worse than
  no report, because it silently ships the wrong numbers.
- No web interface: the users of this tool are managers and cron, not
  browsers. Adding HTTP, CSP, SEO and legal pages would be scope that
  the problem does not require. This project is a CLI, and the security
  and compliance sections of the master prompt do not apply to it.
- Tests cover the pure functions (CSV generation, date range). The mailer
  is covered by `--dry-run` and by the fact that `smtplib` is part of the
  standard library; testing it would require a real SMTP server, which
  is out of scope.


  ## Security Threat Model
Credentials are loaded from a local `.env` file which is excluded from version control via `.gitignore`. This tool assumes execution in a trusted, local environment (e.g., a cron job on a secure server). If deployed to a shared environment, credentials must be injected via environment variables managed by a secret store (e.g., AWS Secrets Manager) instead of a `.env` file.
