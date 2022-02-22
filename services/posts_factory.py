from services.posts_db_repo import PostsDb
from services.seed import blogPosts

class PostsFactory:
    def __init__(self, is_test):
        self.is_test = is_test
        
    def create(self):
        if (self.is_test):
            return blogPosts
        return PostsDb()