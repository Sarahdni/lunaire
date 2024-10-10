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
            "personal_info": {
                "email": user_info['email'],
                "name": user_info.get('name', 'Unknown'),
                "age": user_info.get('age', user_info.get('what is your age', 'Unknown')),
                "country": user_info.get('country', user_info.get('which country do you live in?', 'Unknown')),
                "language": "en"  # Vous pouvez ajouter une logique pour déterminer la langue
            },
            "cycle_info": {
                "last_period_date": datetime.strptime(user_info.get('last_period_date', ''), "%Y-%m-%d"),
                "period_duration": int(user_info.get('period_duration', 0)),
                "cycle_length": int(user_info.get('cycle_length', 28)),
                "cycle_history": []
            },
            "calendar_info": {
                "calendar_type": user_info.get('calendar_service', 'ical').lower(),
                "calendar_url": "",
                "last_generated": None
            },
            "updated_at": datetime.utcnow()
        }

        try:
            result = self.users_collection.update_one(
                {"personal_info.email": user_info['email']},
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

    def update_user_calendar(self, email, calendar_type, calendar_url):
        result = self.users_collection.update_one(
            {"personal_info.email": email},
            {
                "$set": {
                    "calendar_info.calendar_type": calendar_type,
                    "calendar_info.calendar_url": calendar_url,
                    "calendar_info.last_generated": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count

    def get_user_by_email(self, email):
        return self.users_collection.find_one({"personal_info.email": email})

   
 