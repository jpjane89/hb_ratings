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
    if "user" in session:
        flash( "%s is logged in." % session['user'])
        return render_template("user_list.html")
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def process_login():
    email = request.form['email']
    user = model.db.query(model.User).filter_by(email = email).first()
    if user:
        session['user'] = user.email
        return redirect("/user_list")
    else:
       flash('Invalid username/password')

    return render_template('login.html')

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

    session["user"] = [email]
    flash ("Welcome %s!" % email)

    return redirect("/user_list")

@app.route("/user_list")
def user_list():
    user_list = model.db.query(model.User).limit(5).all()
    return render_template("user_list.html", users=user_list)

if __name__ == "__main__":
    app.run(debug=True)