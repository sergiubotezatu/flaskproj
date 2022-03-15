from models.post import Preview
from services.ipost_repo import IPostRepo
from models.post import Post
from services.resources import Services

class PostsEnumerator():
    def __init__(self, posts):
        self.posts = list(posts.items())
        self.counter = -1
        self.limit = -len(self.posts)

    def __next__(self):
        if self.counter >= self.limit:
            result = self.posts[self.counter]
            self.counter -= 1
            return result
        raise StopIteration

def singleton(cls):
    __instances = {}
    def wrapper(*args, **kwargs):
        if cls not in __instances:
            __instances[cls] = cls(*args, **kwargs)
        return __instances[cls]
    return wrapper

@singleton
class Posts(IPostRepo):
    @Services.get
    def __init__(self):
        self.__posts = {}
        
    def add_post(self, post):
        post_id = post.auth[:2] + str(len(self.__posts) + 1)
        self.__posts.update({post_id : post})
        return post_id

    def get_post(self, post_id) -> Post:
        return self.__posts[post_id]

    def __len__(self):
        return len(self.__posts)

    def __iter__(self):
        return PostsEnumerator(self.__posts)

    def remove(self, post_id):
        self.__posts.pop(post_id)

    def replace(self, post_id, post):
        self.__posts[post_id].edit(post)

    def get_user_posts(self, user_name):
        user_posts = []
        for posts in self.__posts:
            if posts.auth == user_name:
                user_posts.append(posts)
        return user_posts

    def get_all(self):
        for posts in self:
            yield (posts[0], Preview(posts[1]))
    
    def delete_all(self):
        self.__posts = {}
    