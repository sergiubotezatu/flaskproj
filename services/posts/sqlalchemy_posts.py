from sqlalchemy import func
from services.database.sqlalchemy import SqlAlchemy
from services.interfaces.ipost_repo import IPostRepo
from services.interfaces.idata_base import IDataBase
from models.post import Post
from services.dependency_inject.injector import Services

class SqlAlchemyPosts(IPostRepo):
    def __init__(self):
        self.db = SqlAlchemy.db
        self.posts = SqlAlchemy.Posts
        self.__count = -1
        
    @property
    def count(self):
        if self.__count == -1:
            return self.db.session.query(self.posts.postid).count()
        return self.__count

    @count.setter
    def count(self, value):
        self.__count = value
                
    def __len__(self):
        return self.count
    
    def add(self, post : Post):
        self.count += 1
        new_post = self.posts(title = post.title, content = post.content, date = post.created, ownerid = post.owner_id)
        self.db.session.add(new_post)
        self.db.session.commit()
        return new_post.postid
        
    def replace(self, id, post : Post):
        dict_new = {"title" : post.title,
                    "content" : post.content,
                    "date_modified" : post.created}
        self.db.session.query(self.posts).filter_by(postid = id).update(dict_new)
        self.db.session.commit()

    def remove(self, id):
        self.db.session.query(self.posts).filter_by(postid = id).delete()
        self.db.session.commit()
    
    def get(self, id, email = None) -> Post:
        displayed = None
        post = None
        if email != None:
            displayed = self.db.query(SqlAlchemy.Deleted.content).filter_by(email = email, deletedid = id).first()
            post = Post(email, "No title", displayed[0])
        else:
            displayed = self.db.session.query\
                        (SqlAlchemy.Users.name,
                        self.posts.title,
                        self.posts.content,
                        SqlAlchemy.Users.ownerid,
                        self.posts.date,
                        self.posts.date_modified).\
                        join(SqlAlchemy.Users, SqlAlchemy.Users.ownerid == self.posts.ownerid).\
                        filter(self.posts.postid == id).first()
            post = Post(displayed[0], displayed[1], displayed[2], owner_id = displayed[3], date = displayed[4])
            post.modified = displayed[5]
        return post

    def get_all(self, page = 0, filters : list = [], max = 5):
        posts = self.db.session.query\
            (self.posts.postid,
            SqlAlchemy.Users.name,
            self.posts.title,
            func.substr(self.posts.content, 0, 150),
            self.posts.ownerid,
            self.posts.date).\
            join(SqlAlchemy.Users, SqlAlchemy.Users.ownerid == self.posts.ownerid).\
            order_by(self.posts.postid.desc())
        print("aaa", posts)
        if len(filters) > 0:
            posts = posts.filter(self.posts.ownerid.in_(filters))
        if page > 0:
            offset = page * max - max
            posts = posts.offset(offset).limit(max + 1)
        return self.__get_fetched(posts.all())
        
    def __get_fetched(self, fetched):
        result = []
        count = 0
        if fetched != None:
            for post in fetched:
                count += 1
                result.append((post[0], Post(post[1], post[2], self.__cut_poem_newlines(post[3]), owner_id= post[4], date = post[5]), count))
        return result

    def __cut_poem_newlines(self, content):
        lines_count = content.count("\n")
        if lines_count > 0:
            chunk = lines_count * 3
            return content[:-chunk] + "[...]"
        return content + "[...]"
