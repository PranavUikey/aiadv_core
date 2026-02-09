from inactive_students import get_inactive_students_mail_data
from mail.render_email import format_email
from mailer import send_email
from tqdm import tqdm
import traceback
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

import os


load_dotenv()

SMTP_ADMIN_EMAIL = os.getenv("SMTP_ADMIN_EMAIL")

# Load template
with open("mail/email.txt", "r") as f:
    email_template = f.read()

last_execution_file = "last_execution.json"

def should_run():
    if not os.path.exists(last_execution_file):
        return True  # First run
    
    with open(last_execution_file, 'r') as f:
        data = json.load(f)
        last_run = datetime.fromisoformat(data['last_run'])
    
    # Check if 3 days have passed
    if datetime.now() - last_run >= timedelta(days=3):
        return True
    return False

def save_execution_time():
    with open(last_execution_file, 'w') as f:
        json.dump({'last_run': datetime.now().isoformat()}, f)



def main():
    data = get_inactive_students_mail_data(days=7)



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
        
        if should_run():
            print("Running inactive student agent...")
            main()  
            save_execution_time()
        else:
            print("Skipping - not 3 days since last execution")
            
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