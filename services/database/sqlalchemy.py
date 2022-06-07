from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.database.database import DataBase
from services.dependency_inject.injector import Services
from services.interfaces.idata_base import IDataBase
from services.interfaces.idatabase_config import IDataBaseConfig
from services.interfaces.idb_upgrade import IDataBaseUpgrade

class SqlAlchemy(DataBase, IDataBase):
    session = None
    Users = None
    Posts = None
    Deleted = None

    @Services.get
    def __init__(self, config : IDataBaseConfig, upgrader : IDataBaseUpgrade):
        super(SqlAlchemy, self).__init__(config, upgrader)
                
    def set_db(self):
        super().set_db()
        self.register_sqlalchemy()
        self.load_models()
        
    def register_sqlalchemy(self):
        SQLALCHEMY_DATABASE_URI = self.db_settings.to_DB_URI()
        SqlAlchemy.engine = create_engine(SQLALCHEMY_DATABASE_URI)
        Session = sessionmaker(autocommit=False, autoflush=True, bind=SqlAlchemy.engine)
        SqlAlchemy.session = Session()        

    @classmethod
    def load_models(cls):
        Base = automap_base()
        Base.prepare(cls.engine, reflect = True)
        cls.Users = Base.classes.blog_users
        cls.Posts = Base.classes.blog_posts
        cls.Deleted = Base.classes.deleted_users
