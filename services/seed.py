from services.posts import Posts
from services import posts_factory
from models.post import Post

blogPosts = Posts()
source_factory = posts_factory.Create("Default")

AUTHOR = "Chandler Bing"
TITLE = "Relaxi-cab"
CONTENT = ("It's so hard to care when you are this relaxed...but maybe you could post something.\n"
"Click me and start writing.")
placeholder = Posts()
placeholder.add_post(Post(AUTHOR, TITLE, CONTENT))
