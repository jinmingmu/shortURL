from sqlalchemy import Column, Integer, String
from database import Base

class URLTable(Base):
    """
    @class URLTable
    Model for a URLTable which defined id, longURL and counter
    """
    __tablename__ = 'URLTable'
    id = Column(Integer, primary_key=True)
    longURL = Column(String(300), unique=True, index=True)
    counter = Column(Integer)

    def __init__(self, longURL=None, counter=None):
        """
        @fn __init__
        init the database columns
        """
        self.longURL = longURL
        self.counter = counter

    def __repr__(self):
        """
        @fn __repr__
        define the return value format
        """
        return "<URLTable(longURL='%s', counter='%d')>" % (self.longURL, self.counter)