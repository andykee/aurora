import json

from sqlalchemy import Column
from sqlalchemy import JSON as SQLAlchemy_JSON

from aurora.models import Data

class JSON(Data):
    __pattern__ = '(?i).*\.json$'

    data = Column(SQLAlchemy_JSON)
    
    def __init__(self, file):
        self.file = file
        
        with open(file.fullpath, 'r') as f:
            self.data = json.loads(f.read())