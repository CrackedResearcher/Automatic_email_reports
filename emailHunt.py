import imaplib
import email
import ai_check as ai
from email.policy import default
import sys
from datetime import datetime, timedelta
import re
import sendemail as send
import emailTemplate as draft
import sqlite3
import reqdInput as setup

DB_path = "user_data.db"

def init_db():
    connect = sqlite3.connect(DB_path)
    c = connect.cursor()
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS user (
        email TEXT NOT NULL,
        app_password TEXT NOT NULL,
        report_sent_to_email TEXT NOT NULL,
        last_run_when TEXT DEFAULT NULL,
        user_interval_run REAL DEFAULT NULL
        )'''
    )
    connect.commit()
    connect.close()


def check_user_exists():
    connect = sqlite3.connect(DB_path)
    c = connect.cursor()
    c.execute('SELECT COUNT(*) FROM user')
    exists = c.fetchone()[0] > 0
    connect.close()
    return exists


def fetch_user_data():
    connect = sqlite3.connect(DB_path)
    c = connect.cursor()
    c.execute('SELECT email, app_password, report_sent_to_email, last_run_when, user_interval_run FROM user LIMIT 1')
    user_data = c.fetchone()
    return user_data


def set_last_runtime(last_run_time, user_email):
    connect = sqlite3.connect(DB_path)
    c = connect.cursor()
    c.execute('UPDATE user SET last_run_when = ? WHERE email = ?',(last_run_time, user_email))
    connect.commit()
    connect.close()


def main_app(user_data):
    user_email = user_data[0]
    app_password = user_data[1]
    report_sent_to_email = user_data[2]

    mail = imaplib.IMAP4_SSL('imap.gmail.com')

    class EmailData:
        def __init__(self, sender="", subject="", email_summary=None, emailType=None, content=""):
            self.sender = sender
            self.subject = subject
            self.email_summary = email_summary
            self.emailType = emailType
            self.content = content

        def set_email_summary(self, summary):
            self.email_summary = summary

        def set_email_type(self, email_type):
            self.emailType = email_type


    class FilteredEmails:
        def __init__(self):
            self.spam = []
            self.important = []
            self.social = []
            self.workEmails = []
            self.personal_Family = []
            self.newsletters_promotions = []

        
        def add_emails(self, category, email):
            category = category.lower().strip()
            if "spam" in category:
                self.spam.append(email)
            elif "important" in category:
                self.important.append(email)
            elif "social" in category:
                self.social.append(email)
            elif "work" in category:
                self.workEmails.append(email)
            elif "personal" in category or "family" in category:
                self.personal_Family.append(email)
            elif "newsletters" in category or "promotions" in category:
                self.newsletters_promotions.append(email)

    all_emails = FilteredEmails()

    received_emails = {}

    try:
        mail.login(user_email, app_password)
        print("Successfully logged in!")

        status, response = mail.select('Inbox')
        if status != 'OK':
            print("Failed to select mailbox")
            mail.logout()
            sys.exit()


        start_date = (datetime.now()-timedelta(1)).strftime("%d-%b-%Y")
        end_date = datetime.now().strftime("%d-%b-%Y")

        search_command = f'(SINCE "{start_date}" BEFORE "{end_date}")'
        status, data = mail.search(None, search_command)


        if status == 'OK':
            email_count = 0
            email_ids = data[0].split()

            for email_id in email_ids:
                email_count+=1
            
                status, data = mail.fetch(email_id, '(RFC822)')
                if status == 'OK':
                    
                    raw_email = data[0][1]
                    msg = email.message_from_bytes(raw_email, policy=default)
                

                    received_emails[f"email_{email_count}"] = EmailData(msg['from'], msg['subject'])


                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                payload = part.get_payload(decode=True).decode()

                                cleaned_content = re.sub(r'https?://\S+\b',"", payload)
                                received_emails[f"email_{email_count}"].content = cleaned_content
                    

                    else:
                        payload = msg.get_payload(decode=True).decode()
                        cleaned_content = re.sub(r'https?://\S+\b', '', payload)
                        received_emails[f"email_{email_count}"].content = cleaned_content
        
        else:
            print("Failed to search emails")

    except imaplib.IMAP4.error as e:
        print(f"Failed to log in: {e}")


    for key, emailData in received_emails.items():
        
        print("-")
        
        categoryRet, emailRet = ai.flag_and_summarize_email(emailData.content, emailData.sender)
        
        all_emails.add_emails(category=categoryRet, email=emailRet)

    print("done reviewing all emails, now crafting a good email to send :)\n")

    getEmail = draft.draftEmail(all_emails)

    send.setLoginCredentials(user_email, app_password, report_sent_to_email)
    send.setEmail(getEmail)

    mail.logout()


def main():
    init_db()
    if not check_user_exists():
        accessedEmail = setup.collect_user_data(DB_path)
        print("\n\nSetup done! You will receive the email at the time you entered.\nNow you can close the terminal :)")
        last_run = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        set_last_runtime(last_run_time=last_run,user_email=accessedEmail)


    user_data = fetch_user_data()
    if user_data:
        user_email = user_data[0]
        last_run_when = user_data[3]
        user_interval_run = user_data[4]
        last_run_time = datetime.strptime(last_run_when, "%d-%b-%Y %H:%M:%S")
        current_time = datetime.now()


        time_difference = current_time - last_run_time

        time_diff = time_difference.total_seconds() / 3600.0

        if time_diff >= user_interval_run:
            main_app(user_data)
            last_run = current_time.strftime("%d-%b-%Y %H:%M:%S")
            set_last_runtime(last_run_time=last_run, user_email=user_email)

        else:
            sys.exit()
            


if __name__ == "__main__":
    main()