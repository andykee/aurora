import os
import datetime

from sqlalchemy import Column, Table, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from aurora.database import Base
from aurora.util import compute_md5


class File(Base):
    __tablename__ = 'file'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ext = Column(String)
    path = Column(String)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    size = Column(Integer)  # The size of the file in bytes
    hash = Column(String(32), unique=True, nullable=True)
    data = relationship('Data', back_populates='file')
    
    def __init__(self, file, compute_hash=True):
        
        self.path, filename = os.path.split(file)
        self.name, ext = os.path.splitext(filename)
        self.ext = ext.lstrip('.').lower()
        
        stats = os.stat(file)
        self.size = stats.st_size
        self.create_time = datetime.datetime.fromtimestamp(stats.st_ctime)
        self.modify_time = datetime.datetime.fromtimestamp(stats.st_mtime)
        if compute_hash:
            self.hash = compute_md5(file)
        
    @property
    def filename(self):
        return self.name + '.' + self.ext
    
    @property
    def fullpath(self):
            return os.path.join(self.path, self.filename)

class DataIdMixin:
    @declared_attr.cascading
    def id(cls):
        if cls.__name__ == 'Data':
            return Column(Integer, primary_key=True)
        else:
            return Column(Integer, ForeignKey('data.id'), primary_key=True)


data_tag = Table('data_tag', Base.metadata,
                 Column('data_id', Integer, ForeignKey('data.id')),
                 Column('tag_id', Integer, ForeignKey('tag.id')))


data_category = Table('data_category', Base.metadata,
                 Column('data_id', Integer, ForeignKey('data.id')),
                 Column('category_id', Integer, ForeignKey('category.id')))


class Data(DataIdMixin, Base):
      
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    @declared_attr
    def __mapper_args__(cls):
        if cls.__name__ == 'Data':
            return {
                    'polymorphic_on':cls.type,
                    'polymorphic_identity':'Data'
            }
        else:
            return {'polymorphic_identity':cls.__name__}

    type = Column(String(50))
    file_id = Column(Integer, ForeignKey('file.id'))
    file = relationship('File', back_populates='data')
    tags = relationship('Tag', secondary=data_tag, back_populates='data')
    categories = relationship('Category', secondary=data_category, back_populates='data')
        

class Tag(Base):
    __tablename__ = 'tag'
    
    id = Column(Integer, primary_key=True)
    _name = Column('name', String, unique=True)
    data = relationship('Data', secondary=data_tag, back_populates='tags')
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value.lower()
        

class Category(Base):
    __tablename__ = 'category'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    #path = ... unique=True.  <- enforce uniqueness of the path, not necissarily of the name (since it's okay to have duplicate names as long as they're not in the same folder)
    data = relationship('Data', secondary=data_category, back_populates='categories')


class DataFactory:
    
    def __init__(self, file, **kwargs):
        self.file = file
        
    def __len__(self):
        raise NotImplementedError
        
    def __getitem__(self, index):
        raise NotImplementedError
