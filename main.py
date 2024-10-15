import os
from datetime import datetime
from utils.language_manager import LanguageManager
from mail_services.email_receiver import connect_to_email, get_unprocessed_emails, parse_email_content, extract_info
from database import user_manager
from calendars import calculate_cycle
from calendars.ical_generator import ICalGenerator
from mail_services.email_sender import send_email_to_user
from utils.logger import logger

def get_last_processed_id():
    # Implement this function to get the last processed email ID
    # For example, you could store this in a database or a file
    pass

def save_last_processed_id(email_id):
    # Implement this function to save the last processed email ID
    # For example, you could store this in a database or a file
    pass

def create_calendar_file(phases, user_info, phase_descriptions, mantras):
    try:
        logger.info("Creating iCal calendar file")
        user_name = user_info.get('name', user_info.get("what's your name?", 'Unknown_User'))
        base_name = f"Cycle_Sync_Calendar_{user_name.replace(' ', '_')}"

        calendar_folder = os.path.join(os.getcwd(), 'generated_calendars')
        os.makedirs(calendar_folder, exist_ok=True)

        user_language = user_info.get('language', 'en')
        logger.info(f"User language before calendar creation: {user_language}")
        
        ical_generator = ICalGenerator()
        calendar_data = ical_generator.generate(phases, user_info, phase_descriptions, mantras)

        file_name = os.path.join(calendar_folder, f"{base_name}.ics")

        with open(file_name, 'wb') as f:
            f.write(calendar_data)

        logger.info(f"Calendar file created: {file_name}")
        return f"file://{os.path.abspath(file_name)}"
    except Exception as e:
        logger.error(f"Error creating calendar file: {str(e)}", exc_info=True)
        raise

def get_email_from_user_info(user_info):
    email_keys = [
        'email',
        "welcome {{slide9ximado}}, what's your email address?",
        "what's your email address?",
        'email address'
    ]
    for key in email_keys:
        if key in user_info:
            return user_info[key]
    return None

def main():
    logger.info("Starting application")
    try:
        language_manager = LanguageManager()

        mail = connect_to_email()
        last_processed_id = get_last_processed_id()
        unprocessed_emails = get_unprocessed_emails(mail, last_processed_id=last_processed_id)
        
        if not unprocessed_emails:
            logger.info("No new emails to process. Ending program.")
            return

        for email_id, email_message in unprocessed_emails:
            try:
                email_content = parse_email_content(email_message)
                logger.info(f"Processing email with ID: {email_id}")
                logger.debug(f"Email content: {email_content}")

                user_info = extract_info(email_content)
                logger.info(f"Extracted user info: {user_info}")

                user_language = user_info.get('language', 'en')
                logger.info(f"User language preference: {user_language}")

                user_email = get_email_from_user_info(user_info)
                if user_email is None:
                    logger.error("Email address not found in extracted user information")
                    continue

                user_info['email'] = user_email

                user_id = user_manager.create_or_update_user(user_info)
                logger.info(f"User created/updated with ID: {user_id}")

                last_period_date_str = user_info.get('last_period_date') or user_info.get('when did your last period start?')
                if not last_period_date_str:
                    logger.error("Last period date not found in user information")
                    continue

                last_period_date = datetime.strptime(last_period_date_str.split('T')[0], "%Y-%m-%d")

                cycle_length = int(user_info['cycle_length'])
                period_duration = int(user_info['period_duration'])

                phases = calculate_cycle(last_period_date, cycle_length, period_duration, num_months=12)
    
                phase_descriptions = language_manager.get_phase_descriptions(user_language)
                mantras = language_manager.get_mantras(user_language)

                calendar_url = create_calendar_file(phases, user_info, phase_descriptions, mantras)
                logger.info(f"Calendar file created: {calendar_url}")

                user_manager.update_user_calendar(user_email, "ical", calendar_url)
                logger.info(f"User calendar information updated")

                send_email_to_user(user_email, calendar_url, user_info.get('name', 'User'), "ical")
                logger.info(f"Email sent to {user_email} with calendar link")

                save_last_processed_id(email_id)
                logger.info(f"Processed email with ID: {email_id}")

            except Exception as e:
                logger.error(f"Error processing email with ID {email_id}: {str(e)}", exc_info=True)

        logger.info("All emails processed successfully")
    except Exception as e:
        logger.error(f"An error occurred during execution: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()