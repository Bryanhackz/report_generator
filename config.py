import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    db_path: str
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    report_sender: str
    report_recipient: str


REQUIRED_KEYS = (
    "DB_PATH",
    "SMTP_HOST",
    "SMTP_PORT",
    "SMTP_USER",
    "SMTP_PASSWORD",
    "REPORT_SENDER",
    "REPORT_RECIPIENT",
)


def _load_dotenv(path: str = ".env") -> None:
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_config() -> Config:
    _load_dotenv()
    missing = [key for key in REQUIRED_KEYS if not os.environ.get(key)]
    if missing:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")
    try:
        port = int(os.environ["SMTP_PORT"])
    except ValueError as exc:
        raise RuntimeError("SMTP_PORT must be an integer") from exc
    return Config(
        db_path=os.environ["DB_PATH"],
        smtp_host=os.environ["SMTP_HOST"],
        smtp_port=port,
        smtp_user=os.environ["SMTP_USER"],
        smtp_password=os.environ["SMTP_PASSWORD"],
        report_sender=os.environ["REPORT_SENDER"],
        report_recipient=os.environ["REPORT_RECIPIENT"],
    )