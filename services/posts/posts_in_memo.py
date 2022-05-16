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
        self.count += 1
        post.id = self.count
        self.__posts.append(post)
        return self.count

    def get(self, post_id, email = None) -> Post:
        for post in self.__posts:
            if int(post_id) == post.id:
                return post

    def __len__(self):
        return len(self.__posts)

    def __iter__(self):
        return PostsEnumerator(self.__posts)

    def remove(self, post_id):
        self.count -= 1
        self.__posts.remove(self.get(post_id))

    def replace(self, post_id, editted : Post):
        index = int(post_id) - 1
        self.__posts[index].auth = editted.auth
        self.__posts[index].title = editted.title
        self.__posts[index].content = editted.content
        self.__posts[index].modified = editted.created            

    def get_all(self, page = 0, filters : list = [], max = 5):
        result = []
        filter_match = lambda x : str(x) in filters if len(filters) > 0 else True
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

    def remove_upon_user_delete(self, id : int):
        result = []
        post : Post
        new_length = 0
        for post in self.__posts:
            if post.owner_id != id:
                result.append(post)
            else:
                new_length += 1
                yield post
        self.count -= new_length
        self.__posts = result