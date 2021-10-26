from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import engine_from_config

app = Flask(__name__)



app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/utopia'
# db = SQLAlchemy(app)

# engine = create_engine('mysql://root:root@localhost/utopia', echo=True)
# Session = sessionmaker(bind=engine)
# BASE = declarative_base()




from utopia import admin_controller, error_handler
