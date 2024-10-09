import unittest
from unittest.mock import patch, MagicMock
from src.database.user_manager import UserManager
from src.database.cycle_manager import CycleManager
from src.database.calendar_manager import CalendarManager

class TestDatabaseManagers(unittest.TestCase):

    def setUp(self):
        self.mock_db_manager = MagicMock()
        self.user_manager = UserManager(self.mock_db_manager)
        self.cycle_manager = CycleManager(self.mock_db_manager)
        self.calendar_manager = CalendarManager(self.mock_db_manager)

    def test_create_or_update_user(self):
        mock_collection = MagicMock()
        self.mock_db_manager.get_user_db.return_value.users = mock_collection
        
        user_info = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': '30',
            'country': 'USA',
            'last_period_date': '2023-05-01T00:00:00.000Z',
            'period_duration': '5',
            'cycle_length': '28',
            'calendar_service': 'google'
        }
        
        result = self.user_manager.create_or_update_user(user_info)
        self.assertIsNotNone(result)
        mock_collection.update_one.assert_called_once()

    def test_save_cycle_data(self):
        mock_collection = MagicMock()
        self.mock_db_manager.get_user_db.return_value.cycles = mock_collection
        
        cycle_data = {'phases': []}
        result = self.cycle_manager.save_cycle_data('john@example.com', cycle_data)
        self.assertIsNotNone(result)
        mock_collection.insert_one.assert_called_once()

    def test_save_calendar_data(self):
        mock_collection = MagicMock()
        self.mock_db_manager.get_user_db.return_value.calendars = mock_collection
        
        calendar_data = {'calendar_url': 'http://example.com/calendar', 'calendar_type': 'ical'}
        result = self.calendar_manager.save_calendar_data('john@example.com', calendar_data)
        self.assertIsNotNone(result)
        mock_collection.insert_one.assert_called_once()

if __name__ == '__main__':
    unittest.main()