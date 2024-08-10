import yaml

class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file

    def load_config(self):
        """Load the configuration from the YAML file."""
        with open(self.config_file, 'r') as file:
            config = yaml.safe_load(file)
        return config

    def save_config(self, config):
        """Save the configuration to the YAML file."""
        with open(self.config_file, 'w') as file:
            yaml.safe_dump(config, file)

    def update_config(self, updates):
        """Update the configuration with the provided parameters."""
        config = self.load_config()
        config.update(updates)
        self.save_config(config)

