from configparser import ConfigParser

class Config:
    def __init__(self):
        self.SECTION = "postgresql"
        self.CONFIGFILE = "db_file"
        self.parser = ConfigParser()
        self.setting_options = ["dbname", "user", "password", "host"]
        
    def load(self):
        if self.section_exists():
            return self.parser.items(self.SECTION)
        else:
            raise Exception(f"Section {self.SECTION} not found in the {self.CONFIGFILE} file")
        
    def save(self):
        self.parser.read(self.CONFIGFILE)
       
    def section_exists(self):
        return self.parser.has_section(self.SECTION)
