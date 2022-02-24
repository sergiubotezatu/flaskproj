from configparser import ConfigParser 

class DataBaseConfig:
    def __init__(self):
        self.config_options = ["host","database", "user","password"]
        self.parser = ConfigParser()
    
    def load_config(self, section, filename = "database.ini"):
        db = {}
        if self.parser.has_section(section):
            params = self.parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(f"Section {section} not found in the {filename} file")

        return db

    def save_config(self, items, section, filename = "database.ini"):
        if not self.parser.has_section(section):
            self.parser.add_section(section)
            for options in self.config_options:
                i = 0
                self.parser.set(section, options, items[i])
                i += 1    
