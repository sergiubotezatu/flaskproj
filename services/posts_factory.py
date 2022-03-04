from services.posts_db_repo import PostsDb
from services.seed import blogPosts

class PostsFactory:
    @staticmethod
    def create(is_test):
        if (is_test):
            return blogPosts
        return PostsDb()

    @staticmethod
    def test():
        pass
    