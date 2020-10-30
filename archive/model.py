from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker

class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=Base)



class File(Base, Serializer):
    id = Column(Integer, primary_key=True)


class Data(Base, Serializer):
    id = Column(Integer, primary_key=True)
