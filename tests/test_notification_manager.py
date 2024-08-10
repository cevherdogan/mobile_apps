import unittest
from src.notification_manager import NotificationManager
from src.config_manager import ConfigManager

class TestNotificationManager(unittest.TestCase):

    def setUp(self):
        self.config_manager = ConfigManager("config/config.yaml")
        self.notification_manager = NotificationManager(self.config_manager)

    def test_send_reminder(self):
        self.notification_manager.send_reminder(
            topic_arn="arn:aws:sns:us-east-1:123456789012:TestTopic",
            days_passed=2
        )
        # Bu testi gerçekleştirmek için email gönderimini doğrulamanız gerekebilir.

    def test_send_deletion_notice(self):
        self.notification_manager.send_deletion_notice(
            topic_arn="arn:aws:sns:us-east-1:123456789012:TestTopic"
        )
        # Bu testi gerçekleştirmek için email gönderimini doğrulamanız gerekebilir.

if __name__ == '__main__':
    unittest.main()


