from models.post import Post
from postRepo.posts import Posts

blogPosts = Posts()

AUTHOR = "Chandler Bing"
TITLE = "Relaxi-cab"
CONTENT = ("It's so hard to care when you are this relaxed...but maybe you could post something.\n"
"Click me and start writing.")
placeholder = Posts()
placeholder.add_post(Post(AUTHOR, TITLE, CONTENT))
