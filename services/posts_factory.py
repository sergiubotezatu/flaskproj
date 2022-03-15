from services.posts_db_repo import PostsDb
from services.seed import blogPosts
from services.ipost_repo import IPostRepo

class PostsFactory:
    @staticmethod
    def create(is_test) -> IPostRepo:
        if (is_test):
            return blogPosts
        return PostsDb()
    