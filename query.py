from model import *
from datetime import datetime

def main(session):
    query1 = session.query(Movie).filter(Movie.date > datetime.datetime.strptime('1970', '%Y')).filter(Movie.date < datetime.datetime.strptime('1973', '%Y')).all()
    print query1

    query2 = session.query(Movie).filter(Movie.title.like('Q%')).all()
    print query2


if __name__ == "__main__":
    s= model.connect()
    main(s)
