from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import engine_from_config

Base = declarative_base()


engine = create_engine('mysql://root:root@localhost/utopia', echo=True)
Session = sessionmaker(bind=engine)