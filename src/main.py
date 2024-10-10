import os
from datetime import datetime

from . import (
    logger,
    connect_to_email, get_latest_email, parse_email_content, extract_info,
    send_email_to_user,
    calculate_cycle, create_ical, create_google_calendar, create_outlook_calendar,
    user_manager, cycle_manager, calendar_manager
)

# Import the necessary functions to load phase descriptions and mantras
from .cycle_calculator import load_phase_descriptions, load_mantras

def create_calendar_file(phases, user_info, calendar_type, phase_descriptions, mantras):
    try:
        base_name = f"{user_info['name'].replace(' ', '_')}_calendar_12months"
        if calendar_type == "ical":
            file_name = f"{base_name}.ics"
            calendar_data = create_ical(phases, user_info, phase_descriptions, mantras)
        elif calendar_type == "google":
            file_name = f"{base_name}_google.csv"
            calendar_data = create_google_calendar(phases, user_info, phase_descriptions, mantras)
        elif calendar_type == "outlook":
            file_name = f"{base_name}_outlook.csv"
            calendar_data = create_outlook_calendar(phases, user_info, phase_descriptions, mantras)
        else:
            raise ValueError(f"Unsupported calendar type: {calendar_type}")
        
        with open(file_name, 'wb') as f:
            f.write(calendar_data)
        
        return f"file://{os.path.abspath(file_name)}"
    except Exception as e:
        logger.error(f"Error creating calendar file: {str(e)}")
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
        # Load phase descriptions and mantras
        phase_descriptions = load_phase_descriptions()
        mantras = load_mantras()

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
        
        user_info['email'] = user_email  # Add email to user_info dictionary
        
        user_id = user_manager.create_or_update_user(user_info)
        logger.info(f"User created/updated with ID: {user_id}")

        last_period_date = user_info['last_period_date']
        cycle_length = int(user_info['cycle_length'])
        period_duration = int(user_info['period_duration'])
        calendar_type = user_info.get('calendar_service', '').lower() or 'ical'  # Default to 'ical' if not specified

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