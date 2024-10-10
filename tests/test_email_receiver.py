import unittest
from unittest.mock import patch, MagicMock
from src.email_receiver import connect_to_email, get_unprocessed_emails, parse_email_content, extract_info, save_last_processed_id, get_last_processed_id

class TestEmailReceiver(unittest.TestCase):

    @patch('src.email_receiver.imaplib.IMAP4_SSL')
    def test_connect_to_email(self, mock_imap):
        mock_imap.return_value.login.return_value = ('OK', [b'Logged in'])
        result = connect_to_email()
        self.assertIsNotNone(result)
        mock_imap.assert_called_once()

    def test_get_unprocessed_emails(self):
        mock_mail = MagicMock()
        mock_mail.search.return_value = ('OK', [b'1 2 3'])
        mock_mail.fetch.return_value = ('OK', [(b'', b'EMAIL_CONTENT')])
        result = get_unprocessed_emails(mock_mail, 'test@example.com')
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, list))

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

    @patch('src.email_receiver.open')
    def test_save_and_get_last_processed_id(self, mock_open):
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        test_id = b'123'
        save_last_processed_id(test_id)
        mock_file.write.assert_called_once_with('123')

        mock_file.read.return_value = '123'
        result = get_last_processed_id()
        self.assertEqual(result, '123')

if __name__ == '__main__':
    unittest.main()