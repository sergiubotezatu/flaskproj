from .post import example 

class postsEnumerator:
    def __init__(self, posts):
        self.posts = list(posts.items())
        self.counter = 0
        self.limit = len(self.posts)

    def __next__(self):
        if self.counter < self.limit:
            result = self.posts[self.counter]
            self.counter += 1
            return result
        raise StopIteration


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

    def __len__(self):
        return len(self.__posts)

    def __iter__(self):
        return postsEnumerator(self.__posts)

blogPosts = Collection()
placeholder = Collection()
placeholder.addPost(example)