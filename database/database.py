from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

## Direct database mode and location
engine = create_engine('mysql+pymysql://root:admin@172.17.0.2:3306/foo', convert_unicode=True)
## Default database session setting
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """
    @fn init_db
    initialize database
    """
    import models
    Base.metadata.create_all(bind=engine)
