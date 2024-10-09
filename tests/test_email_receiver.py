import unittest
from unittest.mock import patch, MagicMock
from src.email_receiver import connect_to_email, get_latest_email, parse_email_content, extract_info

class TestEmailReceiver(unittest.TestCase):

    @patch('src.email_receiver.imaplib.IMAP4_SSL')
    def test_connect_to_email(self, mock_imap):
        mock_imap.return_value.login.return_value = ('OK', [b'Logged in'])
        result = connect_to_email()
        self.assertIsNotNone(result)
        mock_imap.assert_called_once()

    @patch('src.email_receiver.imaplib.IMAP4_SSL')
    def test_get_latest_email(self, mock_imap):
        mock_mail = MagicMock()
        mock_mail.search.return_value = ('OK', [b'1 2 3'])
        mock_mail.fetch.return_value = ('OK', [(b'', b'EMAIL_CONTENT')])
        
        result = get_latest_email(mock_mail, 'test@example.com')
        self.assertIsNotNone(result)

    def test_parse_email_content(self):
        mock_email = MagicMock()
        mock_email.get_payload.return_value = b'Test content'
        mock_email.is_multipart.return_value = False
        
        result = parse_email_content(mock_email)
        self.assertEqual(result, 'Test content')

    def test_extract_info(self):
        email_content = "Name: John Doe\nEmail: john@example.com\nAge: 30"
        result = extract_info(email_content)
        self.assertEqual(result, {
            'Name': 'John Doe',
            'Email': 'john@example.com',
            'Age': '30'
        })

if __name__ == '__main__':
    unittest.main()