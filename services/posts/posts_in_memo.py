from werkzeug.datastructures import FileStorage
from models.post import Preview
from services.interfaces.ipost_repo import IPostRepo
from models.post import Post
from services.posts.images.img_inmemo import ImagesInMemo
from werkzeug.datastructures import FileStorage

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
        self.__posts : list[Post] = []
        self.count = 0
        self.free_ids = [1]
        self.images = ImagesInMemo()
        
    def add(self, post, img : FileStorage = None):
        self.__rmv_placeholder()
        self.count += 1
        post.id = self.free_ids[0]
        post.img_src = self.get_image(img)
        self.__posts.append(post)
        self.free_ids.remove(post.id)
        if not self.free_ids:
            self.free_ids = [self.__posts[-1].id + 1]
        return post.id

    def get(self, post_id, email = None) -> Post:
        post : Post
        for post in self.__posts:
            if int(post_id) == post.id:
                post_copy = Post(post.auth, post.title, post.content, post.owner_id, post.created)
                post_copy.modified = post.modified
                post_copy.img_src = self.images.get(post.img_src)
                post_copy.id = post.id
                return post_copy

    def get_image(self, img : FileStorage):
        if img:
            return self.images.add(img)

    def __len__(self):
        return len(self.__posts)

    def __iter__(self):
        return PostsEnumerator(self.__posts)

    def remove(self, post_id):
        self.free_ids.insert(0, int(post_id))
        for i in range (0, self.count):
            if self.__posts[i].id == int(post_id):
                self.images.remove(self.__posts[i].img_src)
                self.__posts.remove(self.__posts[i])
                break
        self.count -= 1

    def replace(self, post : Post, img : FileStorage):
        for i in range(0, len(self.__posts)):
            if self.__posts[i].id == int(post.id):
                if img:
                    changed_name = self.images.edit(img, post.img_src)
                    if changed_name:
                        self.__posts[i].img_src = changed_name
                self.__posts[i].auth = post.auth
                self.__posts[i].title = post.title
                self.__posts[i].content = post.content
                self.__posts[i].modified = post.created            

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

    def __rmv_placeholder(self):
        if self.count == 1 and self.__posts[0].auth == "Chandler Bing":
            self.remove(1)

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