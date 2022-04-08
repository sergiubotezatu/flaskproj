from models.post import Preview
from services.interfaces.ipost_repo import IPostRepo
from models.post import Post
from services.dependency_inject.injector import Services

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

    def replace(self, post_id, editted : Post):
        self.__posts[post_id].auth = editted.auth
        self.__posts[post_id].title = editted.title
        self.__posts[post_id].content = editted.content
        self.__posts[post_id].modified = editted.created            

    def get_all(self):
        for posts in self:
            yield (posts[0], Preview(posts[1]))
    
    def delete_all(self):
        self.__posts = {}

    def get_user_posts(self, id):
        return super().get_user_posts(id)

    def get_with_posts(self):
        return super().get_with_posts()
    
    def reflect_user_changes(self, id, new_name):
        for posts in self:
            if posts[1].owner_id == id:
                posts[1].auth = new_name
