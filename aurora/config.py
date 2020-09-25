from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from aurora.database import Base

class Config(Base):
    autolaunch_browser = Column(Boolean, nullable=False)
    ignore_duplicates = Column(Boolean, nullable=False)

    def __init__(self):
        self.autolaunch_browser = True
        self.ignore_duplicates = True