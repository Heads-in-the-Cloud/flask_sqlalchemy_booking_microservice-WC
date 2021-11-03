from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utopia import app

engine = create_engine(f"mysql://{app.config['DB_USER']}:{app.config['DB_USER_PASSWORD']}@{app.config['DB_HOST']}/{app.config['DB']}")
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():

    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import utopia.models.booking
    import utopia.models.flights
    import utopia.models.users
    Base.metadata.create_all(bind=engine)

