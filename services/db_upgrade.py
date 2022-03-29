from services.idata_base import IDataBase
from services.resources import Services
from psycopg2 import DatabaseError

class DataBaseUpgrade:
    @Services.get
    def __init__(self, db : IDataBase):
        self.db = db
        self.config = db.config

    def get_version_difference(self):
        upgrades_needed = 0
        try:
            self.db.connect()
            for query in self.steps_needed():
                self.db.cursor.execute(query)
                if bool(self.db.cursor.fetchone()) == True:
                    break
                upgrades_needed += 1
            self.commit_and_close()  
        except (Exception, DatabaseError) as error:
            print(error)
        return upgrades_needed

    def steps_needed(self):
        return ( """
        SELECT EXISTS(
        SELECT OwnerID
        FROM blog_posts)        
        """,
        """
        SELECT EXISTS(
        SELECT OwnerID
        FROM blog_posts
        Where OwnerID = Null)        
        """,
        """
        SELECT EXISTS(
        SELECT Email
        FROM blog_users
        WHERE Email = 'default@admin')        
        """        
        )