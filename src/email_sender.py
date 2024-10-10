from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import logging
from config import EMAIL, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT

logger = logging.getLogger(__name__)

def send_email_to_user(user_email, calendar_url, user_name, calendar_type):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = user_email
    msg['Subject'] = "Your 12-month personalized menstrual calendar"

    calendar_instructions = {
    "ical": "Open the .ics file with your preferred calendar application.",
    "apple": "Open the .ics file with Apple Calendar.",
    "google": "Import the CSV file into Google Calendar by going to Settings > Import & Export.",
    "outlook": "Import the CSV file into Outlook by going to File > Open & Export > Import/Export."
    }

    body = f"""
    Hello {user_name},

    Your 12-month personalized menstrual calendar is ready!

    You can download your calendar by clicking on the following link:
    {calendar_url}

    Instructions to import your calendar:
    {calendar_instructions.get(calendar_type, "Follow your calendar application's instructions to import the file.")}

    This calendar will help you plan and track your menstrual cycles for a full year. Feel free to consult it regularly and adjust it if necessary.

    If you have any questions or need help, don't hesitate to contact us.

    Thank you for using our application!

    The Lunaire Team
    """

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL, user_email, text)
        server.quit()
        logger.info(f"Email successfully sent to {user_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {user_email}: {str(e)}")
        raise

    return True