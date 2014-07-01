import model
from model import *
from datetime import datetime

def main(session):
    query1 = session.query(Movie).filter(Movie.release_date > datetime.strptime('1970', '%Y')).filter(Movie.release_date < datetime.strptime('1973', '%Y')).all()
    for q in query1:
        print q.title, q.release_date

    query2 = session.query(Movie).filter(Movie.title.like('Q%')).all()
    for q in query2:
        print q.title


if __name__ == "__main__":
    s= model.connect()
    main(s)
