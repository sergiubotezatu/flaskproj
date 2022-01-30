from packages import createBlog

blog = createBlog()
blog.secret_key = "FlaskBlog"

if __name__ == ("__main__"):
    blog.run(debug = True)
