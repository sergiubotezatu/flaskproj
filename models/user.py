from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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
    def password(self, userPass):
        self.hashed_pass = generate_password_hash(userPass)
    
    def set_pass(self, userPass, hashed = True):
        if hashed == False:
            self.hashed_pass = userPass
        else:
            self.password = userPass

    def check_pass(self, userPass):
        print(generate_password_hash(userPass))
        print(self.hashed_pass)
        print(userPass)
        return check_password_hash(self.hashed_pass, userPass)
        
    def date_created(self, date):
        if date == None:
            date = datetime.now().strftime("%d/%b/%y %H:%M:%S")
        return date
    

    def edit(self, editted, pwd = None):
        self.name = editted.name
        self.email = editted.email
        self.modified = editted.created
        if pwd != None: 
            self.password = pwd
    
    def serialize(self, id):
        self.id = id