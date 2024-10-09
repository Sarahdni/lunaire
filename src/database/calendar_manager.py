from pymongo.errors import OperationFailure
import logging

logger = logging.getLogger(__name__)

class CalendarManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def save_calendar_data(self, email, calendar_data):
        db = self.db_manager.get_user_db(email)
        calendars_collection = db.calendars
        try:
            result = calendars_collection.insert_one(calendar_data)
            logger.info(f"Calendar data saved with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except OperationFailure as e:
            logger.error(f"Error saving calendar data: {e}")
            raise