import unittest
from unittest.mock import patch, MagicMock
from src.main import main

class TestMainIntegration(unittest.TestCase):

    @patch('src.main.connect_to_email')
    @patch('src.main.get_latest_email')
    @patch('src.main.parse_email_content')
    @patch('src.main.extract_info')
    @patch('src.main.user_manager.create_or_update_user')
    @patch('src.main.calculate_cycle')
    @patch('src.main.create_calendar_file')
    @patch('src.main.cycle_manager.save_cycle_data')
    @patch('src.main.calendar_manager.save_calendar_data')
    @patch('src.main.send_email_to_user')
    def test_main_integration(self, mock_send_email, mock_save_calendar, mock_save_cycle, 
                              mock_create_calendar, mock_calculate_cycle, mock_create_user, 
                              mock_extract_info, mock_parse_email, mock_get_email, mock_connect):
        # Setup mocks
        mock_connect.return_value = MagicMock()
        mock_get_email.return_value = MagicMock()
        mock_parse_email.return_value = "Email content"
        mock_extract_info.return_value = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'last_period_date': '2023-05-01T00:00:00.000Z',
            'cycle_length': '28',
            'period_duration': '5',
            'calendar_service': 'google'
        }
        mock_create_user.return_value = 'user_id'
        mock_calculate_cycle.return_value = []
        mock_create_calendar.return_value = 'http://example.com/calendar'
        mock_save_cycle.return_value = 'cycle_id'
        mock_save_calendar.return_value = 'calendar_id'
        mock_send_email.return_value = True

        # Run main function
        main()

        # Assert all steps were called
        mock_connect.assert_called_once()
        mock_get_email.assert_called_once()
        mock_parse_email.assert_called_once()
        mock_extract_info.assert_called_once()
        mock_create_user.assert_called_once()
        mock_calculate_cycle.assert_called_once()
        mock_create_calendar.assert_called_once()
        mock_save_cycle.assert_called_once()
        mock_save_calendar.assert_called_once()
        mock_send_email.assert_called_once()

if __name__ == '__main__':
    unittest.main()