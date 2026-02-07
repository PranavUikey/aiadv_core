import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_HOST") or os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Safety tuning for Hostinger
MAX_RETRIES = 3
RETRY_DELAY = 15      # seconds between retries
SEND_DELAY = 10       # seconds between successful sends


def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Returns True if email DATA was sent to SMTP server.
    """

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            msg = MIMEMultipart("alternative")
            msg["From"] = f"AIAdventures Training Head <{SMTP_EMAIL}>"
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "html"))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=60) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(SMTP_EMAIL, SMTP_PASSWORD)
                server.send_message(msg)

            print(f"✅ Email sent to {to_email}")
            time.sleep(SEND_DELAY)
            return True

        except smtplib.SMTPDataError as e:
            # DATA already sent → treat as delivered
            print(f"⚠️ SMTPDataError AFTER send for {to_email}: {e}")
            return True

        except smtplib.SMTPException as e:
            print(f"❌ SMTP error for {to_email}: {e}")
            return False

