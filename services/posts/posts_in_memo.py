from models.post import Preview
from services.interfaces.ipost_repo import IPostRepo
from models.post import Post
from services.dependency_inject.injector import Services

class PostsEnumerator():
    def __init__(self, posts : list):
        self.posts = posts
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
        self.__posts = []
        self.count = 0
        
    def add(self, post):
        post_id = self.count + 1
        post.id = post_id
        self.__posts.append(post)
        self.count += 1
        return post_id

    def get(self, post_id) -> Post:
        post_id = int(post_id)
        return self.__posts[post_id - 1]

    def __len__(self):
        return len(self.__posts)

    def __iter__(self):
        return PostsEnumerator(self.__posts)

    def remove(self, post_id):
        post_id = int(post_id) - 1
        self.count -= 1
        self.__posts.remove(self.__posts[post_id])

    def replace(self, post_id, editted : Post):
        post_id = int(post_id) - 1
        self.__posts[post_id].auth = editted.auth
        self.__posts[post_id].title = editted.title
        self.__posts[post_id].content = editted.content
        self.__posts[post_id].modified = editted.created            

    def get_all(self, page = 0, filters : list = [], pagination : bool = True, max = 5):
        result = []
        count = 0
        filter_match = lambda x : True if len(filters) == 0 else lambda x : x in filters
        for post in self.__posts:
            count += 1
            if filter_match(post.id):
                result.append((post.id, Preview(post), count))
            if pagination == True and count == max + 1:
                break
        return result

    def reflect_user_changes(self, id, new_name):
        for posts in self:
            if posts.owner_id == id:
                posts.auth = new_name
