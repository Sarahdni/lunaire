import os
from datetime import datetime
from utils.language_manager import LanguageManager
from mail_services.email_receiver import connect_to_email, get_unprocessed_emails, parse_email_content, extract_info
from database import user_manager
from calendars import calculate_cycle, CalendarFactory
from mail_services.email_sender import send_email_to_user
from utils.logger import logger

# Mock function to get the last processed email ID (to be implemented as needed)
def get_last_processed_id():
    return None

# Mock function to save the last processed email ID (to be implemented as needed)
def save_last_processed_id(email_id):
    logger.info(f"Mock: Saving last processed email ID {email_id}")

# Function to create a calendar file
def create_calendar_file(phases, user_info, language_manager):
    try:
        logger.info("Creating iCal calendar file")
        user_name = user_info.get('name', user_info.get("what's your name?", 'Unknown_User'))
        base_name = f"Cycle_Sync_Calendar_{user_name.replace(' ', '_')}"

        calendar_folder = os.path.join(os.getcwd(), 'generated_calendars')
        os.makedirs(calendar_folder, exist_ok=True)

        user_language = user_info.get('language', 'en')
        logger.info(f"User language before calendar creation: {user_language}")
        
        phase_descriptions = language_manager.get_phase_descriptions(user_language)
        mantras = language_manager.get_mantras(user_language)

        calendar_generator = CalendarFactory.get_generator("ical")
        calendar_data = calendar_generator.generate(phases, user_info, phase_descriptions, mantras)

        file_name = os.path.join(calendar_folder, f"{base_name}.ics")

        with open(file_name, 'wb') as f:
            f.write(calendar_data)

        logger.info(f"Calendar file created: {file_name}")
        return f"file://{os.path.abspath(file_name)}"
    except Exception as e:
        logger.error(f"Error creating calendar file: {str(e)}", exc_info=True)
        raise

# Function to retrieve user's email from the extracted info
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

# Main function to test the email processing and calendar generation
def main():
    logger.info("Starting test application")
    try:
        language_manager = LanguageManager()

        # Step 1: Connect to email
        mail = connect_to_email()
        last_processed_id = get_last_processed_id()
        
        # Step 2: Retrieve unprocessed emails
        unprocessed_emails = get_unprocessed_emails(mail, last_processed_id=last_processed_id)
        
        if not unprocessed_emails:
            logger.info("No new emails to process. Ending test.")
            return

        # Step 3: Process each email
        for email_id, email_message in unprocessed_emails:
            try:
                email_content = parse_email_content(email_message)
                logger.info(f"Processing email with ID: {email_id}")
                logger.debug(f"Email content: {email_content}")

                user_info = extract_info(email_content)
                logger.info(f"Extracted user info: {user_info}")

                # Step 4: Get user language preference
                user_language = user_info.get('language', 'en')
                logger.info(f"User language preference: {user_language}")

                # Step 5: Extract email address
                user_email = get_email_from_user_info(user_info)
                if user_email is None:
                    logger.error("Email address not found in extracted user information")
                    continue

                user_info['email'] = user_email

                # Step 6: Update or create the user in the database
                user_id = user_manager.create_or_update_user(user_info)
                logger.info(f"User created/updated with ID: {user_id}")

                # Step 7: Extract last period date
                last_period_date_str = user_info.get('last_period_date') or user_info.get('when did your last period start?')
                if not last_period_date_str:
                    logger.error("Last period date not found in user information")
                    continue

                # Step 8: Parse the date
                last_period_date = datetime.strptime(last_period_date_str.split('T')[0], "%Y-%m-%d")

                # Step 9: Calculate cycle
                cycle_length = int(user_info['cycle_length'])
                period_duration = int(user_info['period_duration'])
                phases = calculate_cycle(last_period_date, cycle_length, period_duration, num_months=12)

                # Step 10: Create and save the calendar file
                calendar_url = create_calendar_file(phases, user_info, language_manager)
                logger.info(f"Calendar file created: {calendar_url}")

                # Step 11: Update user calendar in the database
                user_manager.update_user_calendar(user_email, "ical", calendar_url)
                logger.info(f"User calendar information updated")

                # Step 12: Send email with calendar link
                send_email_to_user(user_email, calendar_url, user_info.get('name', 'User'), "ical")
                logger.info(f"Email sent to {user_email} with calendar link")

                # Step 13: Mark the email as processed
                save_last_processed_id(email_id)
                logger.info(f"Processed email with ID: {email_id}")

            except Exception as e:
                logger.error(f"Error processing email with ID {email_id}: {str(e)}", exc_info=True)

        logger.info("All emails processed successfully")
    except Exception as e:
        logger.error(f"An error occurred during test execution: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()
