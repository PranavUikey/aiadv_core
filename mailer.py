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


def send_email(to_email: str, subject: str, body: str):
    """
    Sends an HTML email using Hostinger SMTP with retries and throttling.
    """

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            msg = MIMEMultipart("alternative")
            msg["From"] = f"AIAdventures – Training & Operations Team <{SMTP_EMAIL}>"
            msg["To"] = to_email
            msg["Subject"] = subject

            # HTML email (required for logo & formatting)
            msg.attach(MIMEText(body, "html"))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=60) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()

                server.login(SMTP_EMAIL, SMTP_PASSWORD)
                server.send_message(msg)

            print(f"✅ Email sent to {to_email}")
            time.sleep(SEND_DELAY)  # throttle (very important)
            return

        except smtplib.SMTPServerDisconnected:
            print(f"⚠️ SMTP disconnected while sending to {to_email} "
                  f"(attempt {attempt}/{MAX_RETRIES})")

            if attempt == MAX_RETRIES:
                raise

            time.sleep(RETRY_DELAY)

        except smtplib.SMTPException as e:
            print(f"❌ SMTP error for {to_email}: {e}")
            raise

        except Exception as e:
            print(f"❌ Unexpected error for {to_email}: {e}")
            raise
