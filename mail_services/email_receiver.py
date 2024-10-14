import imaplib
import email
from bs4 import BeautifulSoup
import re
from datetime import datetime
from config import EMAIL, EMAIL_PASSWORD, IMAP_SERVER, NOTIFICATION_EMAIL
from utils.logger import logger

def connect_to_email():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, EMAIL_PASSWORD)
        return mail
    except Exception as e:
        logger.error(f"Error connecting to email: {str(e)}")
        return None

def get_unprocessed_emails(mail, sender_email=None, last_processed_id=None):
    if sender_email is None:
        sender_email = NOTIFICATION_EMAIL
    
    logger.info(f"Searching for unprocessed emails from {sender_email}")
    mail.select('inbox')
    
    search_criteria = f'(FROM "{sender_email}")'
    if last_processed_id:
        search_criteria += f' UID {last_processed_id}:*'
    
    _, search_data = mail.search(None, search_criteria)
    email_ids = search_data[0].split()
    
    if not email_ids:
        logger.info(f"No unprocessed emails found from {sender_email}")
        return []
    
    emails = []
    for email_id in email_ids:
        _, msg_data = mail.fetch(email_id, "(RFC822)")
        email_body = msg_data[0][1]
        email_message = email.message_from_bytes(email_body)
        emails.append((email_id, email_message))
    
    logger.info(f"Found {len(emails)} unprocessed emails from {sender_email}")
    return emails

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
        elif key == "hi, what's your first name?":
            key = 'name'
        elif key == "when is your birthday, {{slide:9ximado}}?":
            key = 'birth_date'
        elif key == "to better understand your cycle, could you share when your last menstrual cycle occurred?":
            key = 'last_period_date'
        
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
    if 'last_period_date' in info:
        info['last_period_date'] = info['last_period_date'][:10]  # Garder seulement la partie date

    if 'how long does your period typically last?' in info:
        info['period_duration'] = int(info['how long does your period typically last?'])

    if "what's the average length of your menstrual cycle?" in info:
        info['cycle_length'] = int(info["what's the average length of your menstrual cycle?"])

    # Traitement spécial pour la langue préférée
    lang_keys = [
        'which language you prefer to receive the calendar in?',
        'preferred language',
        'language'
    ]
    
    lang_key = 'Which language you prefer to receive the calendar in?'
    if lang_key in info:
        lang_value = info[lang_key].strip()
        lang_mapping = {
            'English': 'en',
            'Français': 'fr',
            'Español': 'es',
            'Nederlands': 'nl',
            'Deutsch': 'de',
            'Italiano': 'it'
        }
        info['language'] = lang_mapping.get(lang_value, 'en')
        logger.info(f"Extracted language value: {lang_value}")
        logger.info(f"Mapped language code: {info['language']}")
    else:
        info['language'] = 'en'
        logger.info("No language preference found, defaulting to English")


    # Traitement spécial pour le service de calendrier
    calendar_key = 'which calendar service would you like to use?'
    if calendar_key in info:
        calendar_value = info[calendar_key].lower()
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
    
    return info