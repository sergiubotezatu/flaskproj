from models.post import Preview
from services.ipost_repo import IPostRepo
from models.post import Post

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


class Posts(IPostRepo):
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

    def get_all(self):
        for posts in self:
            yield (posts[0], Preview(posts[1]))
    
    def delete_all(self):
        self.__posts = {}
    