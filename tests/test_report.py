import unittest
from unittest.mock import patch
from config import Config
from mailer import send_report

class MailerTests(unittest.TestCase):
    @patch('smtplib.SMTP_SSL')
    def test_send_report(self, mock_smtp_ssl):
        mock_instance = mock_smtp_ssl.return_value.__enter__.return_value
        
        config = Config(
            db_path=":memory:", smtp_host="smtp.example.com", smtp_port=465,
            smtp_user="user", smtp_password="pass",
            report_sender="from@test.com", report_recipient="to@test.com"
        )
        
        send_report(config, "Test Subject", "Test Body", "a,b,c\n1,2,3", "test.csv")
        
        mock_instance.login.assert_called_once_with("user", "pass")
        mock_instance.send_message.assert_called_once()
        
        message = mock_instance.send_message.call_args[0][0]
        self.assertEqual(message['Subject'], "Test Subject")
        self.assertEqual(message['To'], "to@test.com")

if __name__ == "__main__":
    unittest.main()
