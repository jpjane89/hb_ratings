from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from correlation import pearson
import random

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

    # def similarity(self, other):
    #     u_ratings = {}
    #     paired_ratings = []
    #     for r in self.ratings:
    #         u_ratings[r.movie_id] = r

    #     for r in other.ratings:
    #         u_r = u_ratings.get(r.movie_id)
    #         if u_r:
    #             paired_ratings.append((u_r.rating, r.rating))

    #     if paired_ratings:
    #         return pearson(paired_ratings)
    #     else:
    #         return 0.0

    def predict_rating(self, movie):
        user_ratings = self.ratings
        similarities = [ (movie.similarity(r.movie), r) for r in user_ratings ]
        similarities.sort(reverse=True)
        similarities = [ sim for sim in similarities if sim[0] > 0 ]
        if not similarities:
            return None
        numerator = sum( [r.rating * similarity for similarity, r in similarities])
        denominator = sum( [similarity[0] for similarity in similarities])
        return numerator/denominator

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key= True)
    title = Column(String(120), nullable=True) 
    release_date = Column(Date, nullable=True)
    imbd_url = Column(String(120), nullable=True)

    def similarity(self, other):
        m_ratings = {}
        paired_ratings = []
        for r in self.ratings:
            m_ratings[r.user_id] = r

        for r in other.ratings:
            m_r = m_ratings.get(r.user_id)
            if m_r:
                paired_ratings.append((m_r.rating, r.rating))

        if paired_ratings:
            return pearson(paired_ratings)
        else:
            return 0.0

    def most_similar(self,movies):
        pearsons = []
        for m in movies:
            sim = self.similarity(m)
            pearsons.append((sim,m))
        pearsons.sort(reverse=True)
        return pearsons[random.randint(1, 10)]

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
    pass


if __name__ == "__main__":
    main()
