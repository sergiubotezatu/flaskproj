from services.dependency_inject.injector import Services
from models.user import User
from services.interfaces.iusers_repo import IUsersRepo
from models.post import Post
from services.interfaces.idata_base import IDataBase

class UsersDb(IUsersRepo):
    @Services.get
    def __init__(self, db : IDataBase):
        self.db = db
        
    def add(self, user : User):
        return self.db.perform("""
    INSERT INTO blog_users(ownerID, Name, Email, Password, Date, Role)      
    VALUES (DEFAULT, %s, %s, %s, %s, %s)
    RETURNING OwnerID;
    """, user.name, user.email, user.hashed_pass, user.created, user.role, fetch="fetchone")[0]        

    def get_posts(self, user_id):
        to_display = self.db.perform("""
            SELECT p.PostID,
                u.Name,
                p.Title,
                SUBSTRING(p.Content, 1, 150),
                p.OwnerID,
                p.Date
                FROM blog_posts p
            INNER JOIN blog_users u
                ON p.OwnerID = u.OwnerID
                AND p.OwnerID = %s
                ORDER BY p.PostID DESC;
            """, user_id, fetch = "fetchall")
        posts = []
        for post in to_display:
            posts.append((post[0],
            Post(
                post[1],
                post[2],
                self.__cut_poem_newlines(post[3]),
                owner_id = user_id,
                date = post[5]
                ))
                )
        return posts

    def get_by(self, **kwargs):
        identifier = ""
        ident_value = None
        if "mail" in kwargs:
            identifier = "Email"
            ident_value = kwargs["mail"]
        else:
            identifier = "OwnerID"
            ident_value = int(kwargs["id"])
        return self.__get_user(identifier, ident_value)

    def __get_user(self, identifier, value):
        displayed = self.db.perform(f"""
        SELECT *
        FROM blog_users
        WHERE {identifier} = """ + "%s", value, fetch = "fetchone")
        if displayed == None:
            return displayed
        user = User(displayed[1], displayed[2], displayed[4], displayed[6])
        user.password = displayed[3]
        user.modified = displayed[5]
        user.id = displayed[0]
        return user

    def remove(self, user : User):
        self.db.perform("""
        INSERT INTO deleted_users
        SELECT u.Email, p.Content 
        FROM blog_posts p
        RIGHT JOIN blog_users u ON p.OwnerId = u.OwnerID
        WHERE u.OwnerID = %s;
        """, user.id)
        self.db.perform("""
        DELETE FROM 
        blog_users
        WHERE OwnerID = %s
        ;
        """, user.id)

    def update(self, usr_id, user : User, pwd = ""):
        change_pass = f", Password = '{pwd}'"if pwd != "" else ""
        change_role = f", Role = '{user.role}'" if user.role != None else ""
        self.db.perform(f"""
        UPDATE blog_users
        SET Name = '{user.name}', Email= '{user.email}', Date_modified = '{user.created}'{change_pass}{change_role}
        WHERE OwnerID = {usr_id};
        """)

    def get_all(self):
        result = self.db.perform("""
        SELECT u.OwnerID, u.Name, u.Role
        FROM blog_users u
        ORDER BY u.OwnerID DESC;
        """, fetch = "fetchall") + self.get_all_inactive()
        return result

    def get_all_inactive(self):
        displayed =  self.db.perform("""
        SELECT DISTINCT Email
        FROM deleted_users
        ;
        """, fetch = "fetchall")
        result = []
        for record in displayed:
            result.append((record[0], record[0]))
        return result

    def get_inactive_posts(self, email):
        displayed = self.db.perform("""
        SELECT d.Content,
        CASE
        WHEN CHAR_LENGTH(d.Content) > 150 THEN SUBSTRING(d.Content, 1, 150)
        ELSE d.Content
        END AS Preview 
        FROM deleted_users AS d
        WHERE Email = %s
        """, email, fetch = "fetchall")
        posts = []
        for record in displayed:
            posts.append((email, Post(email, "No title", record[0], owner_id = email)))
        return posts       

    def has_account(self, user_id) -> bool:
        return self.db.perform("""
        SELECT EXISTS(
        SELECT OwnerID
        FROM blog_users
        WHERE OwnerID = %s)
    """, user_id, fetch = "fetchone")

    def get_inactive(self, email):
        result = self.db.perform("""
        SELECT Email
        FROM deleted_users
        WHERE Email = %s;
        """, email, fetch = "fetchone")
        email : str = result[0]
        name = email[0:email.index("@")]
        return User(name, email)

    def __cut_poem_newlines(self, content):
        if content == None:
            return ''
        lines_count = content.count("\n")
        if lines_count > 0:
            chunk = lines_count * 3
            return content[:-chunk] + "[...]"
        return content + "[...]"
