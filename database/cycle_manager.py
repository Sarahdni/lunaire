from pymongo.errors import OperationFailure
from utils.logger import logger

class CycleManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def save_cycle_data(self, email, cycle_data):
        db = self.db_manager.db
        cycles_collection = db.cycles
        try:
            result = cycles_collection.insert_one(cycle_data)
            logger.info(f"Cycle data saved with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except OperationFailure as e:
            logger.error(f"Error saving cycle data: {e}")
            raise

    def get_cycle_history(self, email):
        db = self.db_manager.db
        cycles_collection = db.cycles
        return list(cycles_collection.find({"email": email}).sort("date", -1))

    def update_cycle(self, cycle_id, updated_data):
        db = self.db_manager.db
        cycles_collection = db.cycles
        result = cycles_collection.update_one({"_id": cycle_id}, {"$set": updated_data})
        return result.modified_count