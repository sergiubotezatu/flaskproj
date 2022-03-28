from datetime import datetime

class User:
    def __init__(self, userName, email, date = None):
        self.id = 0
        self.name = userName
        self.email = email
        self.hashed_pass = ""
        self.created = self.date_created(date)
        self.modified = ""
    
    @property
    def password(self):
        raise AttributeError("Password can not be read.")

    @password.setter
    def password(self, hashed):
        self.hashed_pass = hashed
        
    def date_created(self, date):
        if date == None:
            date = datetime.now().strftime("%d/%b/%y %H:%M:%S")
        return date    