from pymongo.errors import OperationFailure
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_or_update_user(self, user_info):
        if 'email' not in user_info:
            raise ValueError("Email is required for user creation/update")

        db = self.db_manager.get_user_db(user_info['email'])
        users_collection = db.users

        user_data = {
            "name": user_info.get('name', 'Unknown'),
            "email": user_info['email'],
            "age": user_info.get('age', user_info.get('what is your age', 'Unknown')),
            "country": user_info.get('country', user_info.get('which country do you live in?', 'Unknown')),
            "last_period_date": self._parse_date(user_info.get('last_period_date', user_info.get('when did your last period start?'))),
            "period_duration": int(user_info.get('period_duration', user_info.get('how long does your period typically last?', 0))),
            "cycle_length": int(user_info.get('cycle_length', user_info.get("what's the average length of your menstrual cycle?", 28))),
            "calendar_service": user_info.get('calendar_service', user_info.get('which calendar service would you like to use?', 'Unknown'))
        }

        try:
            result = users_collection.update_one(
                {"email": user_info['email']},
                {"$set": user_data},
                upsert=True
            )
            if result.upserted_id:
                logger.info(f"New user created with ID: {result.upserted_id}")
            else:
                logger.info(f"Existing user updated with email: {user_info['email']}")

            self.db_manager.ensure_collections_exist(db)
            return str(result.upserted_id or result.modified_count)
        except OperationFailure as e:
            logger.error(f"Error creating/updating user: {e}")
            raise

    def _parse_date(self, date_string):
        if not date_string:
            return None
        try:
            return datetime.strptime(date_string.split('T')[0], "%Y-%m-%d")
        except ValueError:
            logger.warning(f"Invalid date format: {date_string}. Using None.")
            return None