import unittest
from src.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):

    def setUp(self):
        self.config_manager = ConfigManager("config/config.yaml")

    def test_load_config(self):
        config = self.config_manager.load_config()
        self.assertIsNotNone(config)

    def test_save_config(self):
        config = self.config_manager.load_config()
        self.config_manager.save_config(config)
        # Burada, dosyanın doğru kaydedildiğini doğrulamak için ek kontrol ekleyebilirsiniz.

    def test_update_config(self):
        updates = {"reminder_days": [2, 5, 7], "deletion_days": 9}
        self.config_manager.update_config(updates)
        config = self.config_manager.load_config()
        self.assertEqual(config['reminder']['day_1'], 2)

if __name__ == '__main__':
    unittest.main()


