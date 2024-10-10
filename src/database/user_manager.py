from pymongo.errors import DuplicateKeyError
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.users_collection = self.db_manager.users_collection

    def create_or_update_user(self, user_info):
        user_data = {
            "name": user_info.get('name', 'Unknown'),
            "email": user_info['email'],
            "age": user_info.get('age', 'Unknown'),
            "country": user_info.get('country', 'Unknown'),
            "cycle_info": {
                "last_period_date": datetime.strptime(user_info.get('last_period_date', ''), "%Y-%m-%d"),
                "period_duration": int(user_info.get('period_duration', 0)),
                "cycle_length": int(user_info.get('cycle_length', 28))
            },
            "calendar_info": {
                "calendar_type": user_info.get('calendar_service', ''),
                "calendar_url": user_info.get('calendar_url', '')
            },
            "updated_at": datetime.utcnow()
        }

        try:
            result = self.users_collection.update_one(
                {"email": user_info['email']},
                {"$set": user_data, "$setOnInsert": {"created_at": datetime.utcnow()}},
                upsert=True
            )
            if result.upserted_id:
                logger.info(f"New user created with ID: {result.upserted_id}")
                return str(result.upserted_id)
            else:
                logger.info(f"Existing user updated with email: {user_info['email']}")
                return str(result.modified_count)
        except DuplicateKeyError:
            logger.error(f"Duplicate email: {user_info['email']}")
            raise
        except Exception as e:
            logger.error(f"Error creating/updating user: {e}")
            raise

    def get_user_by_email(self, email):
        return self.users_collection.find_one({"email": email})

    def update_user_calendar(self, email, calendar_type, calendar_url):
        result = self.users_collection.update_one(
            {"email": email},
            {
                "$set": {
                    "calendar_info.calendar_type": calendar_type,
                    "calendar_info.calendar_url": calendar_url,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count

    def update_user_cycle(self, email, last_period_date, period_duration, cycle_length):
        result = self.users_collection.update_one(
            {"email": email},
            {
                "$set": {
                    "cycle_info.last_period_date": datetime.strptime(last_period_date, "%Y-%m-%d"),
                    "cycle_info.period_duration": int(period_duration),
                    "cycle_info.cycle_length": int(cycle_length),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count

 