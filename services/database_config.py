from configparser import ConfigParser
from models.db_settings import DBSettings
from services.idatabase_config import IDataBaseConfig
from services.resources import Services
from services.config import Config

class DataBaseConfig(Config, IDataBaseConfig):
    is_configured = False

    @Services.get
    def __init__(self):
        super().__init__()
        self.settings = None
        self.current_config = None
        #self.load_existing_section()
        
    def add_settings(self, settings : DBSettings):
        self.settings = settings
                    
    def load(self):
        self.current_config = {}
        super().load(self.current_config)
        self.edit_config_status()

    def save(self):
        super().save(self.settings)

    def load_existing_section(self):
        if super().section_exists:
            self.load()
       
    @classmethod
    def edit_config_status(cls):
        cls.is_configured = True
