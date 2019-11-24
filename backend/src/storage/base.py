import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

pg_connection_string = 'postgresql://' + os.environ.get('POSTGRES_USER') + ':' +\
    os.environ.get('POSTGRES_PASSWORD') + '@db/' + os.environ.get('POSTGRES_DB')
engine = create_engine(pg_connection_string, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
