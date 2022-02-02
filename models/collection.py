class Collection:
    def __init__(self):
        self.__posts = {}

    def addPost(self, post):
        id = post.auth[:2] + str(len(self.__posts) + 1)
        self.__posts.update({id : post})

    def getPost(self, id):
        return self.__posts[id]
    
    def getIds(self):
        return list(self.__posts.keys())    