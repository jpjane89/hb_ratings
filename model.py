from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import sessionmaker

ENGINE = None
Session = None

Base = declarative_base()

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True)
    email = Column(String(64), nullable= True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key= True)
    title = Column(String(120), nullable=True) 
    release_date = Column(Date, nullable=True)
    imbd_url = Column(String(120), nullable=True)

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key= True)
    user_id = Column(Integer, nullable=True)
    movie_id = Column(Integer, nullable=True)
    rating = Column(Float, nullable=True)

### End class declarations

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
