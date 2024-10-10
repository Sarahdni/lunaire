import os
from datetime import datetime

from . import (
    logger,
    connect_to_email, get_latest_email, parse_email_content, extract_info,
    send_email_to_user,
    user_manager, cycle_manager, calendar_manager
)

from .cycle_calculator import load_phase_descriptions, load_mantras, create_ical, create_google_calendar, create_outlook_calendar, create_apple_calendar, calculate_cycle

def create_calendar_file(phases, user_info, calendar_type, phase_descriptions, mantras):
    try:
        print(f"Creating calendar file for type: {calendar_type}")
        base_name = f"{user_info['name'].replace(' ', '_')}_calendar_12months"
        
        calendar_folder = os.path.join(os.getcwd(), 'calendars')
        os.makedirs(calendar_folder, exist_ok=True)
        
        if calendar_type == "ical":
            file_name = os.path.join(calendar_folder, f"{base_name}.ics")
            calendar_data = create_ical(phases, user_info, phase_descriptions, mantras)
        elif calendar_type == "apple":
            file_name = os.path.join(calendar_folder, f"{base_name}.ics")
            calendar_data = create_apple_calendar(phases, user_info, phase_descriptions, mantras)
        elif calendar_type == "google":
            file_name = os.path.join(calendar_folder, f"{base_name}_google.csv")
            calendar_data = create_google_calendar(phases, user_info, phase_descriptions, mantras)
        elif calendar_type == "outlook":
            file_name = os.path.join(calendar_folder, f"{base_name}_outlook.csv")
            calendar_data = create_outlook_calendar(phases, user_info, phase_descriptions, mantras)
        else:
            raise ValueError(f"Unsupported calendar type: {calendar_type}")
        
        with open(file_name, 'wb') as f:
            f.write(calendar_data)
        
        print(f"Calendar file created: {file_name}")
        return f"file://{os.path.abspath(file_name)}"
    except Exception as e:
        print(f"Error creating calendar file: {str(e)}")
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
        phase_descriptions = load_phase_descriptions()
        mantras = load_mantras()
        logger.info(f"Loaded mantras structure: {type(mantras)}")
        if isinstance(mantras, dict):
            logger.info(f"First level keys: {list(mantras.keys())}")
            logger.info(f"Sample mantra: {mantras['Menstrual']['January'][0]}")
        else:
            logger.error(f"Mantras is not a dictionary, it's a {type(mantras)}")

        mail = connect_to_email()
        email_message = get_latest_email(mail)
        if email_message is None:
            logger.warning("No new email found. Ending program.")
            return
        
        email_content = parse_email_content(email_message)
        logger.info(f"Full email content: {email_content}")
        
        user_info = extract_info(email_content)
        logger.info(f"Extracted user info: {user_info}")

        user_email = get_email_from_user_info(user_info)
        if user_email is None:
            logger.error("Email address not found in extracted user information")
            return
        
        user_info['email'] = user_email

        user_id = user_manager.create_or_update_user(user_info)
        logger.info(f"User created/updated with ID: {user_id}")

        last_period_date = user_info['last_period_date']
        cycle_length = int(user_info['cycle_length'])
        period_duration = int(user_info['period_duration'])
        calendar_type = user_info.get('calendar_service', '').lower() or 'ical'

        phases = calculate_cycle(last_period_date, cycle_length, period_duration, num_months=12)
        
        calendar_url = create_calendar_file(phases, user_info, calendar_type, phase_descriptions, mantras)
        logger.info(f"Calendar file created: {calendar_url}")

        user_manager.update_user_calendar(user_email, calendar_type, calendar_url)
        logger.info(f"User calendar information updated")

        send_email_to_user(user_email, calendar_url, user_info['name'], calendar_type)
        logger.info(f"Email sent to {user_email} with calendar link")

        logger.info("Processing completed successfully")
    except Exception as e:
        logger.error(f"An error occurred during execution: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()