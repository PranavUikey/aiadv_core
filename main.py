from inactive_students import get_inactive_students_mail_data
from mail.render_email import format_email
from mailer import send_email
from tqdm import tqdm
import traceback
from dotenv import load_dotenv
import json
import os


load_dotenv()

SMTP_ADMIN_EMAIL = os.getenv("SMTP_ADMIN_EMAIL")

# Load template
with open("mail/email.txt", "r") as f:
    email_template = f.read()


def main():
    data = get_inactive_students_mail_data(days=7)
    if not os.path.exists("sent_log.json"):
        with open("sent_log.json", "w") as f:
            json.dump([], f)

    print(f"Preparing emails for {len(data)} users...\n")

    for user_data in tqdm(data):
        to_email = user_data["user"]["email"]
        subject = "Let’s get you back on track 🚀 with AI Adventures!"

        body = format_email(email_template, user_data)

        # DRY RUN
        
        # print("✅ DRY RUN: Email content for this user:")
        # print("=" * 80)
        #     print(f"TO: {to_email}")
        #     print(body)
        

        send_email(to_email, subject, body)

        

    print("\nDone.")
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("❌ Agent failed with error:")
        print(e)
        traceback.print_exc()

        try:

            send_email(
                to=SMTP_ADMIN_EMAIL,
                subject="🚨 AIAdventures Inactive Student Agent Failed",
                body=f"The agent failed with error:\n\n{e}\n\nCheck GitHub Actions logs."
            )
        except Exception:
            pass

        raise