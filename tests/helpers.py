from flask.testing import FlaskClient
from models.post import Post
from models.user import User
from services.database.database import DataBase
from services.posts.posts_in_memo import Posts
from services.users.users_in_memo import Users

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
    query_index = url.rfind("/?")
    if query_index != -1:
        url = url.replace(url[query_index:], "")
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

def add_disposable_post():
    return Posts().add(Post("John Doe", "Generic", "I will be deleted"))

def add_disposable_user():
    return Users().add(User("James Doe", "James@mail"))
    