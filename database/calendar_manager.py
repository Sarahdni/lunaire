from pymongo.errors import OperationFailure
from utils.logger import logger

class CalendarManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def save_calendar_data(self, email, calendar_data):
        db = self.db_manager.db
        calendars_collection = db.calendars
        try:
            result = calendars_collection.insert_one(calendar_data)
            logger.info(f"Calendar data saved with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except OperationFailure as e:
            logger.error(f"Error saving calendar data: {e}")
            raise

    def get_user_calendar(self, email):
        db = self.db_manager.db
        calendars_collection = db.calendars
        return calendars_collection.find_one({"email": email})

    def update_calendar(self, calendar_id, updated_data):
        db = self.db_manager.db
        calendars_collection = db.calendars
        result = calendars_collection.update_one({"_id": calendar_id}, {"$set": updated_data})
        return result.modified_count