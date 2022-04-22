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
        self.page_count = 0
        self.__posts = {}
        
    def add(self, post):
        post_id = post.auth[:2] + str(len(self.__posts) + 1)
        self.__posts.update({post_id : post})
        return post_id

    def get(self, post_id) -> Post:
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

    def get_all(self, page = 0, filters : list = [], pagination : bool = True, max = 5):
        result = []
        count = 0
        filter_match = lambda x : True if len(filters) == 0 else lambda x : x in filters
        for posts in self:
            count += 1
            if filter_match(posts[0]):
                result.append((posts[0], Preview(posts[1]), count))
            if pagination == True and count == max + 1:
                break
        return result
    
    def delete_all(self):
        self.__posts = {}
    
    def reflect_user_changes(self, id, new_name):
        for posts in self:
            if posts[1].owner_id == id:
                posts[1].auth = new_name
