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
        return self.query.perform("insertion", user.name, user.email, user.password, user.created)[0]        

    def get_posts(self, user_id):
        to_display = self.query.perform("get_user_posts", user_id)
        posts = []
        for post in to_display:
            posts.append((post[0],
            Post(
                post[1],
                post[2],
                self.__cut_poem_newlines(post[7]),
                owner_id = user_id,
                date = post[4]
                ))
                )
        
        return posts

    def get_user_by_mail(self, mail):
        displayed = self.query.perform("get_by_mail", mail)
        if displayed == None:
            return displayed
        user = User(displayed[1], displayed[2], displayed[3], displayed[4])
        user.serialize(displayed[0])
        return user

    def get_user_by_id(self, id):
        displayed = self.query.perform("get_by_id", id)
        if displayed == None:
            return displayed
        user = User(displayed[1], displayed[2], displayed[3], displayed[4])
        user.serialize(displayed[0])
        return user        

    def remove_user(self, user : User):
        self.query.perform("archive", user.id)
        self.query.perform("deletion", user.id)

    def update_user(self, usr_id, user : User, pwd = None):
        if pwd == None:
            self.query.perform("change_pass", pwd, usr_id)
        self.query.perform("edit", user.name, user.email, user.created, usr_id, usr_id)

    def get_all(self):
        return self.query.perform("get_users")

    def delete_from_archive(self):
        return self.query.perform("admin_delete")

    def __cut_poem_newlines(self, content):
        print("Y---", type(content))
        lines_count = content.count("\n")
        if lines_count > 0:
            chunk = lines_count * 3
            return content[:-chunk] + "[...]"
        return content + "[...]"

class QueryUsers:
    def __init__(self, db : IDataBase):
        self.db = db
    
    def perform(self, request, *args):
        retrieved = 0
        execution = self.__queries()[request]
        try:
            self.db.connect()
            self.db.cursor.execute(execution, args)
            retrieved = self.__fetch_if_needed(request)
            self.db.commit_and_close()
        except (Exception, DatabaseError) as error:
            print(error)
        return retrieved
    
    def __queries(self):
        return {
        "insertion" : self.__insertion(),
        "edit" : self.__update(),
        "deletion" : self.__delete(),
        "archive" : self.__archive(),
        "get_users" : self.__get_all_users(),
        "get_by_mail" : self.__get_user_by_identifier("Email"),
        "get_by_id" : self.__get_user_by_identifier("OwnerID"),
        "get_user_posts" : self.__read_all(),
        "change_pass" : self.__change_password(),
        "admin_delete" : self.__complete_deletion()
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

    def fetch_user(self, *user_id) -> Post:
        result = None
        try:
            self.db.connect()
            self.db.cursor.execute(self.__get_user(), user_id)
            result = self.db.cursor.fetchone()
            self.db.commit_and_close()
        except (Exception, DatabaseError) as error:
            print(error)
        print(type(result))
        print(result)    
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


    def __read_all(self):
        return """
        SELECT p.*,
        CASE
        WHEN CHAR_LENGTH(p.Content) > 150 THEN SUBSTRING(p.Content, 1, 150)
        ELSE p.Content
        END AS Preview 
        FROM blog_posts AS p
        WHERE OwnerID = %s
        ORDER BY p.PostID DESC;
        """

    def __insertion(self):
        return """
        INSERT INTO blog_users      
        VALUES (DEFAULT, %s, %s, %s, %s)
        RETURNING OwnerID;
        """

    def __update(self):
        return """
            UPDATE blog_users
            SET Name = %s, Email= %s, Date_modified = %s
            WHERE OwnerID = %s;
            UPDATE blog_posts
            SET Author = blog_users.Name
            FROM blog_users
            WHERE blog_posts.OwnerID = blog_users.OwnerID AND blog_posts.OwnerID = %s;
            """

    def __change_password(self):
        return """
            UPDATE blog_users
            SET Password = %s
            WHERE OwnerID = %s;
        """
    
    def __archive(self):
        return """
        INSERT INTO deleted_users(Email, Content)
        SELECT u.Email, p.Content 
        FROM blog_posts p
        INNER JOIN blog_users u ON p.OwnerId = u.OwnerID
        Where p.OwnerID = %s;
        """

    def __delete(self):
        return """
            DELETE FROM 
            blog_users
            WHERE OwnerID = %s;
            """

    def __get_user_by_identifier(self, identifier : str):
        return f"""
        SELECT *
        FROM blog_users
        WHERE {identifier} = """ + "%s"

    def __get_all_users(self):
        return """
        SELECT OwnerID, Name
        FROM blog_users
        ORDER BY OwnerID DESC;
        """

    def __complete_deletion(self):
        return """
        DELETE FROM deleted_users
        WHERE deleted_at < now() - interval '180 days'
        """

    def __fetch_if_needed(self, request):
        result = []
        if request == "get_users" or request == "get_user_posts":
            result = self.db.cursor.fetchall()
        if request == "get_by_mail" or request == "get_by_id" or request == "insertion":
            result = self.db.cursor.fetchone()
        return result
