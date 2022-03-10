from resources.posts_db_repo import PostsDb
from resources.seed import blogPosts
from resources.ipost_repo import IPostRepo

class PostsFactory:
    @staticmethod
    def create(is_test) -> IPostRepo:
        if (is_test):
            return blogPosts
        return PostsDb()
    