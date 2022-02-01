from post import Post

class User:

    def __init__(self, userName, password):
        self.userName = userName
        self.__password = password
        self.__posts = {}

    def checkPass(self, userPass):
        return self.__password == userPass

    def addPost(self, post):
        id = self.userName[:2] + str(len(self.__posts) + 1)
        self.__posts.update({id : post})
        