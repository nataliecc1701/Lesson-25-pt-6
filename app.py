
# Library imports
from flask import Flask, render_template, redirect, session, flash
from sqlalchemy.exc import IntegrityError

# Local imports
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm
from config import configure_app

app = Flask(__name__)

configure_app(app)
connect_db(app)

# Routes
@app.route("/")
def redir_index():
    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User.register(username = form.username.data,
                                 pwd = form.password.data,
                                 email = form.email.data,
                                 first_name = form.first_name.data,
                                 last_name = form.last_name.data)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("username and email must be unique")
            return render_template("register.html", form=form)
        session["username"] = new_user.username
        return redirect(f"/users/{new_user.username}")
        
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid username/password']
        
    return render_template("login.html", form=form)

@app.route("/secret")
def show_secret():
    if "username" in session:
        return("You made it!")
    else:
        return redirect("/register")
    
@app.route("/logout")
def log_out_user():
    session.pop("username")
    return redirect("/")

@app.route("/users/<username>")
def show_user_info(username):
    if "username" not in session:
        return redirect("/")
    user = User.query.get_or_404(username)
    return render_template("userinfo.html", user=user)