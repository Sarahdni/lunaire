import os
from datetime import datetime

from . import (
    logger,
    connect_to_email, get_latest_email, parse_email_content, extract_info,
    send_email_to_user,
    calculate_cycle, create_ical, create_google_calendar, create_outlook_calendar,
    user_manager, cycle_manager, calendar_manager
)

def create_calendar_file(phases, user_info, calendar_type):
    try:
        base_name = f"{user_info['name'].replace(' ', '_')}_calendar_12months"
        if calendar_type == "ical":
            file_name = f"{base_name}.ics"
            calendar_data = create_ical(phases, user_info)
        elif calendar_type == "google":
            file_name = f"{base_name}_google.csv"
            calendar_data = create_google_calendar(phases, user_info)
        elif calendar_type == "outlook":
            file_name = f"{base_name}_outlook.csv"
            calendar_data = create_outlook_calendar(phases, user_info)
        else:
            raise ValueError(f"Unsupported calendar type: {calendar_type}")
        
        with open(file_name, 'wb') as f:
            f.write(calendar_data)
        
        return f"file://{os.path.abspath(file_name)}"
    except Exception as e:
        logger.error(f"Error creating calendar file: {str(e)}")
        raise

def main():
    logger.info("Starting application")
    try:
        mail = connect_to_email()
        email_message = get_latest_email(mail)
        if email_message is None:
            logger.warning("No new email found. Ending program.")
            return
        
        email_content = parse_email_content(email_message)
        logger.info(f"Full email content: {email_content}")

        user_info = extract_info(email_content)
        logger.info(f"Extracted user info: {user_info}")

        user_id = user_manager.create_or_update_user(user_info)
        logger.info(f"User database created/updated: {user_id}")

        if 'email' not in user_info:
            logger.error("Email address not found in extracted user information")
            return

        try:
            cycle_start = datetime.strptime(user_info['last_period_date'], "%Y-%m-%dT%H:%M:%S.%fZ")
            cycle_length = int(user_info['cycle_length'])
            period_length = int(user_info['period_duration'])
            calendar_type = user_info['calendar_service'].lower()
        except KeyError as e:
            logger.error(f"Missing data in user information: {str(e)}")
            raise ValueError(f"Incomplete user data: {str(e)}")
        except ValueError as e:
            logger.error(f"Error converting user data: {str(e)}")
            raise ValueError(f"Invalid user data: {str(e)}")

        phases = calculate_cycle(cycle_start, cycle_length, period_length, num_months=12)
        
        calendar_url = create_calendar_file(phases, user_info, calendar_type)
        logger.info(f"Calendar file created: {calendar_url}")

        cycle_id = cycle_manager.save_cycle_data(user_info['email'], {"phases": phases})
        calendar_id = calendar_manager.save_calendar_data(user_info['email'], {"calendar_url": calendar_url, "calendar_type": calendar_type})
        logger.info(f"Cycle and calendar data saved. IDs: {cycle_id}, {calendar_id}")

        send_email_to_user(user_info['email'], calendar_url, user_info['name'], calendar_type)
        logger.info(f"Email sent to {user_info['email']} with calendar link")

        logger.info("Processing completed successfully")
    except Exception as e:
        logger.error(f"An error occurred during execution: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()