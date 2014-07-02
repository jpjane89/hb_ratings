import model
import csv
from datetime import datetime

def load_users(session):
    # use u.user
    with open('seed_data/u.user', 'rb') as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            user = model.User(id = row[0], age = row[1], zipcode = row[4])
            session.add(user)
    session.commit()

def load_movies(session):
    # use u.item
    with open('seed_data/u.item', 'rb') as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            title = row[1].split("(")
            title = title[0].strip()
            title = title.decode("latin-1")
            date = row[2]
            if date:
                date_object = datetime.strptime(date, '%d-%b-%Y')
                movie = model.Movie(id = row[0],title = title, release_date= date_object, imbd_url=row[4])
            else:
                movie = model.Movie(id = row[0],title = title, imbd_url=row[4])
            
            session.add(movie)
    
    session.commit()

def load_ratings(session):
    # use u.data
    with open('seed_data/u.data', 'rb') as f:
        reader = csv.reader(f, delimiter= '\t') 
        for row in reader:
            rate = model.Rating(user_id = row[0], movie_id = row[1], rating=row[2])
            session.add(rate)
    
    session.commit()

def main(session):
    load_users(session)
    load_movies(session)
    load_ratings(session)

if __name__ == "__main__":
    main(model.db)
