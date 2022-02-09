from __init__ import create_blog

blog = create_blog()
blog.secret_key = "FlaskBlog"

if __name__ == ("__main__"):
    blog.run(debug = True)
