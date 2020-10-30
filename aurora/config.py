from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from aurora.database import Base

FILES_TO_IGNORE = ['*.DS_Store']



class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True)
    autolaunch_browser = Column(Boolean, nullable=False)
    ignore_duplicates = Column(Boolean, nullable=False)

    def default(self):
        self.autolaunch_browser = True
        self.ignore_duplicates = True