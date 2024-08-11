import unittest
from src.topic_manager import TopicManager
from src.config_manager import ConfigManager

class TestTopicManager(unittest.TestCase):

    def setUp(self):
        self.config_manager = ConfigManager("config/config.yaml")
        self.topic_manager = TopicManager(self.config_manager)

    def test_create_topic(self):
        result = self.topic_manager.create_topic("TestTopic")
        self.assertIsNotNone(result)

    def test_delete_topic(self):
        topic_arn = self.topic_manager.create_topic("TestTopic")
        self.topic_manager.delete_topic(topic_arn)
        # Burada, topiğin başarıyla silindiğini doğrulamak için ek kontrol ekleyebilirsiniz.

if __name__ == '__main__':
    unittest.main()

