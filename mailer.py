import smtplib
from email.message import EmailMessage

from config import Config


def send_report(
    config: Config,
    subject: str,
    body: str,
    csv_content: str,
    filename: str,
) -> None:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = config.report_sender
    message["To"] = config.report_recipient
    message.set_content(body)
    message.add_attachment(
        csv_content.encode("utf-8"),
        maintype="text",
        subtype="csv",
        filename=filename,
    )

    if config.smtp_port == 465:
        client = smtplib.SMTP_SSL(config.smtp_host, config.smtp_port, timeout=30)
    else:
        client = smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=30)
        client.starttls()

    with client:
        client.login(config.smtp_user, config.smtp_password)
        client.send_message(message)