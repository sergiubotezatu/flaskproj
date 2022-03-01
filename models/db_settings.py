
class DBSettings:
    def __ini__(self, settings):
        self.section = settings[0]
        self.host = settings[1]
        self.database = settings[2]
        self.user = settings[3]
        self.password = settings[4]

    def params_list(self):
        return [self.host, self.database, self.user, self.password]