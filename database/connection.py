from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import MONGO_URI
from utils.logger import logger

class DatabaseManager:
    def __init__(self):
        self.client = self._initialize_database()
        self.db = self.client['LUNAIRE']
        self.users_collection = self.db['users']
        self._ensure_collection_exists()

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

    def _ensure_collection_exists(self):
        if 'users' not in self.db.list_collection_names():
            self.db.create_collection('users')
            logger.info("Collection 'users' created in LUNAIRE database")
        else:
            logger.debug("Collection 'users' already exists in LUNAIRE database")

    def create_index(self):
        self.users_collection.create_index("email", unique=True)
        logger.info("Unique index on 'email' created for 'users' collection")

    def close_connection(self):
        self.client.close()
        logger.info("MongoDB connection closed")
