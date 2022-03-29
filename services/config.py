from configparser import ConfigParser

class Config:
    def __init__(self):
        self.SECTION = "postgresql"
        self.CONFIGFILE = "db_file"
        self.parser = ConfigParser()
        self.setting_options = ["dbname", "user", "password", "host"]

    def load(self, config):
        section = self.SECTION
        self.parser.read(self.CONFIGFILE)
        if self.section_exists():
            params = self.parser.items(section)
            for param in params:
                config[param[0]] = param[1]
        else:
            raise Exception(f"Section {section} not found in the {self.CONFIGFILE} file")

    def save(self, settings):
        if not self.section_exists():
            section = self.SECTION
            params = f"[{section}]\n"
            for options in self.setting_options:
                params += f"{options} = {getattr(settings, options)}\n"
            with open(self.CONFIGFILE, "w") as writer:
                writer.write(params)

    def section_exists(self):
        return self.parser.has_section(self.SECTION)
