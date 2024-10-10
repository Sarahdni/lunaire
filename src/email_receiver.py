import imaplib
import email
from config import EMAIL, EMAIL_PASSWORD, IMAP_SERVER, NOTIFICATION_EMAIL
from bs4 import BeautifulSoup
import re
from datetime import datetime

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
    soup = BeautifulSoup(email_content, 'html.parser')
    info = {}

    for b_tag in soup.find_all('b'):
        key = b_tag.text.strip().replace(':', '').lower()
        if key == "welcome {{slide:9ximado}}, what's your email address":
            key = 'email'
        
        i_tag = b_tag.find_next('i')
        if i_tag:
            value = i_tag.text.strip()
            if 'Entered Text:' in value:
                value = value.replace('Entered Text:', '').strip()
            info[key] = value
        else:
            next_tag = b_tag.find_next()
            if next_tag and next_tag.name != 'b':
                info[key] = next_tag.text.strip()

    # Traitement spécial pour certains champs
    if "what's your name?" in info:
        info['name'] = info.pop("what's your name?")

    if 'when did your last period start?' in info:
        date_str = info['when did your last period start?']
        info['last_period_date'] = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")

    if 'how long does your period typically last?' in info:
        info['period_duration'] = int(info['how long does your period typically last?'])

    if "what's the average length of your menstrual cycle?" in info:
        info['cycle_length'] = int(info["what's the average length of your menstrual cycle?"])

    # Traitement spécial pour le service de calendrier
    calendar_key = 'which calendar service would you like to use?'
    if calendar_key in info:
        calendar_value = info[calendar_key].lower()
        print(f"Raw calendar value: {calendar_value}")
        if 'google' in calendar_value:
            info['calendar_service'] = 'google'
        elif 'outlook' in calendar_value:
            info['calendar_service'] = 'outlook'
        elif 'apple' in calendar_value:
            info['calendar_service'] = 'apple'
        else:
            info['calendar_service'] = 'ical'
    else:
        info['calendar_service'] = 'ical'  # Valeur par défaut
    
    print(f"Final calendar service: {info['calendar_service']}")

    return info