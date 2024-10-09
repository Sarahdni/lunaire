from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import MONGO_URI
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.client = self._initialize_database()

    @staticmethod
    def _initialize_database():
        logger.info(f"Initializing MongoDB connection with URI: {MONGO_URI}")
        if not MONGO_URI.startswith(('mongodb://', 'mongodb+srv://')):
            logger.error(f"Invalid MongoDB URI: {MONGO_URI}")
            raise ValueError(f"Invalid MongoDB URI: {MONGO_URI}. URI must start with 'mongodb://' or 'mongodb+srv://'")
        try:
            client = MongoClient(MONGO_URI)
            client.admin.command('ismaster')  # This will raise an exception if the connection fails
            logger.info("MongoDB connection established successfully")
            return client
        except ConnectionFailure as e:
            logger.error(f"Error connecting to MongoDB: {e}")
            raise

    def get_user_db(self, email):
        db_name = f"user_{email.replace('@', '_').replace('.', '_')}"
        return self.client[db_name]

    @staticmethod
    def ensure_collections_exist(db):
        collections_to_create = ["users", "cycles", "calendars"]
        for collection_name in collections_to_create:
            if collection_name not in db.list_collection_names():
                db.create_collection(collection_name)
                logger.info(f"Collection {collection_name} created in {db.name}")
            else:
                logger.debug(f"Collection {collection_name} already exists in {db.name}")