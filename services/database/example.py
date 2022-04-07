from configparser import ConfigParser
from models.db_settings import DBSettings


class DataBaseConfig():                                
    def __init__(self):
        super().__init__()
        self.setting_options = ["dbname", "user", "password", "host"]

    def load(self, settings : DBSettings):
        self.current_config = {}
        params = super().load(settings.section)
        for param in params:
            self.current_config[param[0]] = param[1]
        
        
    def save(self, settings : DBSettings):
        parser = ConfigParser()
        parser.add_section(settings.section)
        for i in range(4):
            parser.set(settings.section,
            f"""{self.setting_options[i]}=
            {getattr(settings, self.setting_options[i])}""")
        super().save(parser)