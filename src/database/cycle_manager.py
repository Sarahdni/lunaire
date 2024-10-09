from pymongo.errors import OperationFailure
import logging

logger = logging.getLogger(__name__)

class CycleManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def save_cycle_data(self, email, cycle_data):
        db = self.db_manager.get_user_db(email)
        cycles_collection = db.cycles
        try:
            result = cycles_collection.insert_one(cycle_data)
            logger.info(f"Cycle data saved with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except OperationFailure as e:
            logger.error(f"Error saving cycle data: {e}")
            raise