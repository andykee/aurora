import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def new_engine(catalog=None):
    if catalog is None:
        return create_engine('sqlite://')
    else:
        return create_engine(f'sqlite://{catalog}')


def new_session(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()