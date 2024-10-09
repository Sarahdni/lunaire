import unittest
from unittest.mock import patch, MagicMock
from src.email_sender import send_email_to_user

class TestEmailSender(unittest.TestCase):

    @patch('src.email_sender.smtplib.SMTP')
    def test_send_email_to_user(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        result = send_email_to_user('user@example.com', 'http://example.com/calendar', 'John Doe', 'ical')
        
        self.assertTrue(result)
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()

if __name__ == '__main__':
    unittest.main()