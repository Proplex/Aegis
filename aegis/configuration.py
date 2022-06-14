import yaml, logging

class Configuration:

    def __init__(self, config_file):
        self.logger = logging.getLogger("AegisConfig")
        self.config_map = ""
        with open(config_file, 'r') as file:
            self.config_map = yaml.safe_load(file)
            self.logger.info("Successfully loaded configuration!")
            self.logger.debug(f"Configuration: {self.config_map}")


    def get(self):
        return self.config_map


