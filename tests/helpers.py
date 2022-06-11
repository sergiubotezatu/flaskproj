from typing import Union
from flask.testing import FlaskClient
from models.post import Post
from models.user import User
from services.database.database import DataBase
from services.dependency_inject.injector import Services
from services.interfaces.ipost_repo import IPostRepo
from services.interfaces.iusers_repo import IUsersRepo

class RepoMngr:
    @Services.get
    def __init__(self, repo : Union[IPostRepo, IUsersRepo]):
        self.repo = repo
        self.ids = []
                
    def create_posts_db(self, count : int, name = "John Doe", owner_id = 2):
        for i in range(count):
            post = Post(name, "Generic", f"Test post {str(i + 1)}", owner_id)
            self.add(post)
        
    def delete(self, id = 0):
        self.repo.remove(id)
        self.ids.remove(id)

    def add(self, entity : Union[Post, User]):
        self.repo.add(entity)
        self.ids.append(entity.id)        

    def clear(self):
        for id in self.ids:
            self.repo.remove(id)
        self.ids = []
        
def log_user(id, name, email, role):
    def decorator(test_func):
        def wrapper(client):
            with client.session_transaction() as session:
                session["id"] = id
                session["username"] = name
                session["email"] = email
                session["role"] = role
            return test_func(client)
        return wrapper
    return decorator

def configure(is_config : bool):
    def decorator(test_func):
        def wrapper(client):
            DataBase.config.is_configured = is_config
            return test_func(client)
        return wrapper
    return decorator

def get_url_userid(result):
    url = result.location
    id_index = url.rfind("/") + 1
    return url[id_index:]
    
def create_posts(client : FlaskClient, name, count :int, title = "Generic-1"):
        post = {
        "author" : name,
        "title" : title,
        "post" : "This is a test"
        }
        for i in range(0, count):
            post["title"] = post["title"].replace(str(i - 1), str(i))
            added = client.post("/post/create", data = post, follow_redirects=False)
            yield get_url_userid(added)
