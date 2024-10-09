from .connection import DatabaseManager
from .user_manager import UserManager
from .cycle_manager import CycleManager
from .calendar_manager import CalendarManager

db_manager = DatabaseManager()
user_manager = UserManager(db_manager)
cycle_manager = CycleManager(db_manager)
calendar_manager = CalendarManager(db_manager)