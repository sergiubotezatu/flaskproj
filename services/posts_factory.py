from services.posts import Posts
from services.posts_table import PostsTable

class Create:
    def __init__(self, is_testing_env):
        self.is_testing_env = is_testing_env

    def create_source(self):
        if (self.is_testing_env == "FlaskTest"):
            return Posts()
        return PostsTable()