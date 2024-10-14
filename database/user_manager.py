from pymongo.errors import DuplicateKeyError
from utils.logger import logger
from datetime import datetime

class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.users_collection = self.db_manager.users_collection

    def create_or_update_user(self, user_info):
        user_data = {
            "personal_info": {
                "email": user_info['email'],
                "name": user_info.get('name', user_info.get("hi, what's your first name?", 'Unknown')),
                "birth_date": self.parse_date(user_info.get('when is your birthday, {{slide9ximado}}?', '')),
                "country": user_info.get('country', user_info.get('which country do you live in?', 'Unknown')),
                "language": user_info.get('language', 'en')
            },
            "cycle_info": {
                "last_period_date": self.parse_date(user_info.get('last_period_date', '')),
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

        # ... rest of the method ...

    

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
    
    def parse_date(self, date_string):
        if not date_string:
            return None
        try:
            return datetime.strptime(date_string[:10], "%Y-%m-%d")
        except ValueError:
            return None