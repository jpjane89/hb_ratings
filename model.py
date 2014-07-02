from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from correlation import pearson

engine = create_engine("sqlite:///ratings.db", echo=False)
db = scoped_session(sessionmaker(bind=engine, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = db.query_property()

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
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    rating = Column(Float, nullable=True)

    user = relationship("User", backref=backref("ratings",order_by=id))
    movie = relationship("Movie", backref=backref("ratings", order_by=id))

### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
