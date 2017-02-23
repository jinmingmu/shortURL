from sqlalchemy import Column, Integer, String
from database import Base

class URLTable(Base):
    __tablename__ = 'URLTable'
    id = Column(Integer, primary_key=True)
    longURL = Column(String(300), unique=True, index=True)
    counter = Column(Integer)

    def __init__(self, longURL=None, counter=None):
        self.longURL = longURL
        self.counter = counter

    def __repr__(self):
        return "<URLTable(longURL='%s', counter='%d')>" % (self.longURL, self.counter)