import psycopg2
from services.idata_base import IDataBase
from services.idatabase_config import IDataBaseConfig
from services.resources import Services

class DataBase(IDataBase):
    config = None

    @Services.get
    def __init__(self, config : IDataBaseConfig):
        DataBase.config = config
        self.conn = None
        self.cursor = None
    
    @classmethod
    def initialize_db(cls, settings):
        cls.config.add_settings(settings)
        cls.config.save()
        cls.config.load()

    def create_database(self, *args):
        try:
            self.connect()
            for operation in self.tables_creation():
                self.cursor.execute(operation, args)
            self.commit_and_close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def connect(self):
        self.conn = psycopg2.connect(**self.config.current_config)
        self.cursor = self.conn.cursor()

    def commit_and_close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
    
    def tables_creation(self):
        return ("""      
            CREATE TABLE IF NOT EXISTS blog_users(
            OwnerID SERIAL PRIMARY KEY,
            Name varchar(30),
            Email varchar(200),
            Password varchar(5000),
            Date varchar(50),
            Date_modified varchar(50));
        """,
            """        
            CREATE TABLE IF NOT EXISTS blog_posts(
            PostID SERIAL PRIMARY KEY,
            Author varchar(30),
            Title varchar(200),
            Content varchar(5000),
            Date varchar(50),
            Date_modified varchar(50),
            OwnerID int,
            FOREIGN KEY (OwnerID) REFERENCES blog_users(OwnerID)
            ON UPDATE CASCADE ON DELETE CASCADE);
        """,
        """    
        do $$
        declare
            first_row record;
            pass text := %s;
            creation_date text := %s;
            id_update text;            
        begin
            SELECT *
            into first_row
            FROM blog_users
            LIMIT 1;

            IF first_row IS NULL THEN

            INSERT INTO blog_users
            VALUES(DEFAULT, 'Admin1', 'default@admin', pass, creation_date);
            
            ELSIF first_row.Email <> 'default@admin' THEN

            INSERT INTO blog_users
            VALUES(1, 'Admin1', 'default@admin', pass, creation_date) 
            ON CONFLICT ON CONSTRAINT blog_users_pkey
            DO 
            UPDATE SET NAME = 'Admin1', Email = 'default@admin', Password = pass, Date = creation_date;
            END IF;
        END;
        $$
        """,
        """        
            CREATE TABLE IF NOT EXISTS deleted_users(
            Email varchar(200),
            Content varchar(5000),
            deleted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP);
        """,
        """
            ALTER TABLE blog_posts
            ADD FOREIGN KEY (OwnerID) REFERENCES blog_users(OwnerID)
            ON UPDATE CASCADE ON DELETE CASCADE;
        """,
        """
            INSERT INTO blog_users (Name, Email, Password)
            SELECT Author, Author || '@dummy.com', Author
            FROM blog_posts
            WHERE blog_posts.OwnerID = NULL;
        """,
        """
            UPDATE blog_posts
            SET OwnerID = blog_users.OwnerID
            FROM blog_users
            WHERE blog_posts.OwnerID = NULL AND blog_users.Email = blog_posts.Author || '@dummy.com'; 
        """,
        """ 
           CREATE OR REPLACE FUNCTION delete_expired_archived() RETURNS trigger
            LANGUAGE plpgsql
        AS $$
        BEGIN
        DELETE FROM deleted_users WHERE deleted_at < NOW() - interval '1 year';
        RETURN NEW;
        END;
        $$;
            DROP TRIGGER IF EXISTS expired_users_delete
            ON public.deleted_users;
            CREATE TRIGGER expired_users_delete
            AFTER INSERT ON deleted_users
            EXECUTE PROCEDURE delete_expired_archived();
        """)
