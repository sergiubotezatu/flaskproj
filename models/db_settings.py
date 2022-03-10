
class DBSettings:
    def __init__(self, settings : list):
        self.SECTION = "postgresql"
        self.host = settings[0]
        self.dbname = settings[1]
        self.user = settings[2]
        self.password = settings[3]
