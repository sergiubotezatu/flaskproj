from psycopg2 import DatabaseError
from services.resources import Services
from models.user import User
from services.iusers import IUsers
from models.post import Post
from services.idata_base import IDataBase
from services.resources import Services

class UsersDb(IUsers):
    @Services.get
    def __init__(self, db : IDataBase):
        self.db = db
        self.query = QueryUsers(db)

    def add_user(self, user : User):
        self.query.perform("insertion", user.name, user.email, user.password, user.created)

    def get_posts(self, user_id):
        return self.query.perform_read(user_id)

    def get_user_by_mail(self, mail):
        return self.query.fetch_user("Email", mail)

    def get_user_by_id(self, id):
        displayed = self.query.fetch_user("OwnerID", id)
        user = User(displayed[1], displayed[2], displayed[3], displayed[4])
        return user

    def remove_user(self, user : User):
        self.query.perform("archive", user.email, user.name)
        self.query.perform("deletion", user)

    def update_user(self, usr_id, user : User, pwd = None):
        self.query.perform("edit", usr_id, user, pwd)

class QueryUsers:
    def __init__(self, db : IDataBase):
        self.db = db
    
    def perform(self, request, *args):
        retrieved = 0
        execution = self.__queries()[request]
        try:
            self.db.connect()
            self.db.cursor.execute(execution, args)
            self.db.commit_and_close()
        except (Exception, DatabaseError) as error:
            print(error)
        return retrieved
    
    def __queries(self):
        return {
        "insertion" : self.__insertion(),
        "edit" : self.__update(),
        "deletion" : self.__delete(),
        "archive" : self.__archive()
        }
    
    def perform_read(self, id) -> Post:
        result = None
        try:
            self.db.connect()
            result = self.__fetch_all_posts(self.__read_all(id))
            self.db.commit_and_close()
        except (Exception, DatabaseError) as error:
            print(error)
        return result

    def fetch_user(self, column, identifier) -> Post:
        result = None
        try:
            self.db.connect()
            result = self.__fetch_one(self.__get_user(column, identifier))
            self.db.commit_and_close()
        except (Exception, DatabaseError) as error:
            print(error)
        return result

    def __fetch_all_posts(self, query):
        self.db.cursor.execute(query)
        nextPost = self.db.cursor.fetchone()
        result = []
        while nextPost is not None:
            result.append(
            (nextPost[0], 
            Post
            (
            nextPost[1],
            nextPost[2],
            self.__cut_poem_newlines(nextPost[7]),
            nextPost[4])
            )
            )
            nextPost = self.db.cursor.fetchone()
        return result

    def __fetch_one(self, query):
        self.db.cursor.execute(query)
        return self.db.cursor.fetchone()  

    def __read_all(self, id):
        return f"""
        SELECT p.* 
        CASE
        WHEN CHAR_LENGTH(p.Content) > 150 THEN SUBSTRING(p.Content, 1, 150)
        ELSE p.Content
        END AS Preview 
        FROM blog_posts AS p
        WHERE ownerID = {id}
        ORDER BY p.PostID DESC;
        """

    def __insertion(self):
        return """
        INSERT INTO blog_users      
        VALUES (DEFAULT, %s, %s, %s, %s);
        """

    def __update(self):
        return """
            UPDATE blog_users
            SET Name = %s, Email= %s, Password = %s Date_modified = %s
            WHERE OwnerID = %s;
        """
    
    def __archive(self):
        return """
        INSERT INTO deleted_users      
        VALUES (%s, %s);
        """

    def __delete(self):
        return """
            DELETE FROM blog_users
            WHERE OwnerID = %s;
            """

    def __get_user(self):
        return """
        SELECT *
        FROM blog_users
        WHERE %s = %s"""
