from flask import Flask, render_template, redirect, request, session, flash, url_for
import jinja2
import model

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    return redirect("/login")

@app.route("/login", methods=["GET"])
def show_login():
    if session.get("user"):
        return redirect("/user_list")
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def process_login():
    email = request.form['email']
    user = model.db.query(model.User).filter_by(email = email).first()
    if user:
        session['user'] = user.email
        session['user_id'] = user.id
        flash ("Welcome %s!" % email)
        return redirect("/user_list")
    else:
       flash('Invalid username/password')

    return render_template('login.html')

@app.route("/logout", methods=["GET"])
def show_logout():
    session['user'] = ''
    session['user_id'] = ''
    return redirect('/')

@app.route("/register", methods=["GET"])
def show_register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def process_register():
    email = request.form.get("email")
    password = request.form.get("password")

    new_user = model.User(email=email, password=password)
    model.db.add(new_user)
    model.db.commit()

    session["user"] = email
    user = model.db.query(model.User).filter_by(email=email).one()
    session["user_id"] = user.id
    flash ("Welcome %s!" % email)

    return redirect("/user_list")

@app.route("/user_list")
def user_list():
    user_list = model.db.query(model.User).limit(10).all()
    movies = model.db.query(model.Movie).order_by(model.Movie.title).limit(10).all()
    return render_template("user_list.html", users=user_list, movies=movies)

@app.route("/ratings_by_user/<int:id>")
def ratings_list(id):
    ratings = model.db.query(model.Rating).filter_by(user_id=id).all()
    return render_template("ratings_list.html", ratings=ratings, user_id = id)

@app.route("/movie_record/<int:id>")
def movie_record(id):
    movie_list = model.db.query(model.Rating).filter_by(movie_id=id).all()
    return render_template("movie_list.html", movie_list=movie_list)

@app.route("/add_rating/<int:id>", methods =['GET'])
def rating_form(id):
    movie = model.db.query(model.Movie).filter_by(id=id).one()
    return render_template("add_rating.html",movie_title=movie.title)

@app.route("/add_rating/<int:id>", methods =['POST'])
def add_rating(id):
    rating = request.form.get("rating")
    new_rating = model.Rating(user_id = session['user_id'], movie_id = id, rating = float(rating))
    model.db.add(new_rating)
    model.db.commit()
    return redirect("/movie_record/"+str(id))

@app.route("/delete_rating/<int:id>")
def delete_record(id):
    movie_id = model.db.query(model.Rating).filter_by(id=id).one()
    model.db.query(model.Rating).filter_by(id=id).delete()
    model.db.commit()
    return redirect("/movie_record/" + str(movie_id.movie_id))

@app.route("/edit_rating/<int:id>", methods=['GET'])
def edit_record_form(id):
    movie = model.db.query(model.Rating).filter_by(id=id).one()
    return render_template("add_rating.html",movie_title=movie.movie.title)

@app.route("/edit_rating/<int:id>", methods=['POST'])
def edit_record(id):
    rating = request.form.get("rating")
    record = model.db.query(model.Rating).filter_by(id=id).one()
    record.rating = rating
    model.db.commit()
    return redirect("/movie_record/" + str(record.movie_id))

if __name__ == "__main__":
    app.run(debug=True)