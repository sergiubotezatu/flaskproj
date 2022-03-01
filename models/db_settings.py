
class DBSettings:
    def __init__(self, settings):
        self.section = settings[0]
        self.host = settings[1]
        self.database = settings[2]
        self.user = settings[3]
        self.password = settings[4]
