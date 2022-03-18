from datetime import datetime

class User:
    user_id = 0
    def __init__(self, userName, email, password, date = None):
        self.id = User.user_id + 1
        self.name = userName
        self.email = email
        self.password = password
        self.created = self.date_created(date)
        self.modified = ""
        User.increment_id()
        
    def date_created(self, date):
        if date == None:
            date = datetime.now().strftime("%d/%b/%y %H:%M:%S")
        return date
    
    def check_pass(self, userPass):
        return self.password == userPass

    def edit(self, editted, pwd = None):
        self.name = editted.name
        self.email = editted.email
        self.modified = editted.created
        if pwd != None: 
            self.password = pwd
    
    @classmethod
    def increment_id(cls):
        cls.user_id += 1