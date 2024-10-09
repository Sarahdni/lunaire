from pymongo.errors import OperationFailure
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_or_update_user(self, user_info):
        db = self.db_manager.get_user_db(user_info['email'])
        users_collection = db.users

        user_data = {
            "name": user_info['name'],
            "email": user_info['email'],
            "age": user_info['age'],
            "country": user_info['country'],
            "last_period_date": datetime.strptime(user_info['last_period_date'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            "period_duration": int(user_info['period_duration']),
            "cycle_length": int(user_info['cycle_length']),
            "calendar_service": user_info['calendar_service']
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