import imaplib
import email
from config import EMAIL, EMAIL_PASSWORD, IMAP_SERVER, NOTIFICATION_EMAIL

def connect_to_email():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, EMAIL_PASSWORD)
        return mail
    except Exception as e:
        print(f"Error connecting to email: {str(e)}")
        return None

def get_latest_email(mail, sender_email=None):
    if sender_email is None:
        sender_email = NOTIFICATION_EMAIL
    
    print(f"Searching for the latest email from {sender_email}")
    mail.select('inbox')
    _, search_data = mail.search(None, f'(FROM "{sender_email}")')
    email_ids = search_data[0].split()
    
    if not email_ids:
        print(f"No emails found from {sender_email}")
        return None
    
    latest_email_id = email_ids[-1]
    _, msg_data = mail.fetch(latest_email_id, "(RFC822)")
    email_body = msg_data[0][1]
    email_message = email.message_from_bytes(email_body)
    print(f"Email found from {sender_email} with subject: {email_message['Subject']}")
    return email_message

def parse_email_content(email_message):
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode()
    else:
        return email_message.get_payload(decode=True).decode()

def extract_info(email_content):
    lines = email_content.split('\n')
    info = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            info[key.strip()] = value.strip()
    return info