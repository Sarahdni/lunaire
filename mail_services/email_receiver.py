import imaplib
import email
from bs4 import BeautifulSoup
import json
import os
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
            if part.get_content_type() == "text/html":
                return part.get_payload(decode=True).decode()
    else:
        return email_message.get_payload(decode=True).decode()

def load_quiz_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'utils', 'quiz_config.json')
    with open(config_path, 'r') as file:
        return json.load(file)

def extract_info(email_content):
    soup = BeautifulSoup(email_content, 'html.parser')
    info = {}
    quiz_config = load_quiz_config()

    for question in quiz_config['questions']:
        b_tag = soup.find('b', string=lambda text: text and question['question'] in text)
        if b_tag:
            value = None
            next_tag = b_tag.find_next()
            
            # Chercher la valeur dans les balises suivantes
            while next_tag and next_tag.name != 'b':
                if next_tag.name == 'i':
                    value = next_tag.text.strip()
                    if 'Entered Text:' in value:
                        value = value.split('Entered Text:', 1)[1].strip()
                    break
                elif next_tag.string and next_tag.string.strip():
                    value = next_tag.string.strip()
                    break
                next_tag = next_tag.next_sibling

            if value:
                if question['type'] == 'date':
                    value = value[:10]  # Keep only the date part
                elif question['type'] == 'integer':
                    try:
                        value = int(value)
                    except ValueError:
                        logger.warning(f"Could not convert {value} to integer for {question['key']}")
                elif question['type'] == 'choice' and 'mapping' in question:
                    value = question['mapping'].get(value, question['mapping'].get('default', value))
                
                info[question['key']] = value
                logger.info(f"Extracted {question['key']}: {value}")
            else:
                logger.warning(f"No value found for question: {question['question']}")

    logger.info(f"Full extracted info: {info}")
    return info

# You can add any additional helper functions or code here if needed

if __name__ == "__main__":
    # This block can be used for testing the functions in this file
    pass