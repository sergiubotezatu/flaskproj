from user import User

class Registered:

    def __init__(self):
        self.__users = []

    def register(self, user):
        self.__users.append(user)

    def searchUser(self, userName):
        for user in self.__users:
            if user.userName == userName:
                return True          
        return False

    def getUserByName(self, userName):
        for user in self.__users:
            if user.userName == userName:
                return user      
