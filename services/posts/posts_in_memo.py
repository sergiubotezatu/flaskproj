from models.post import Preview
from services.interfaces.ipost_repo import IPostRepo
from models.post import Post


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
        index = int(post_id) - 1
        self.count -= 1
        self.__posts.remove(self.__posts[index])

    def replace(self, post_id, editted : Post):
        index = int(post_id) - 1
        self.__posts[index].auth = editted.auth
        self.__posts[index].title = editted.title
        self.__posts[index].content = editted.content
        self.__posts[index].modified = editted.created            

    def get_all(self, page = 0, filters : list = [], max = 5):
        result = []
        filter_match = lambda x : x in filters if len(filters) > 0 else True
        matches_found = 0
        posts_count = 0
        offset = page * max - max
        for post in self:
            if filter_match(post.owner_id):
                matches_found += 1
                if matches_found >= offset + 1:
                    posts_count += 1
                    result.append((post.id, Preview(post), posts_count))
            if page != 0 and posts_count == max + 1:
                break
        return result


    def reflect_user_changes(self, id, new_name):
        for posts in self:
            if posts.owner_id == id:
                posts.auth = new_name
