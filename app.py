
# Library imports
from flask import Flask, render_template, redirect, session, flash
from sqlalchemy.exc import IntegrityError

# Local imports
from models import connect_db, db, User
from forms import RegisterForm
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
        new_user = User.register(username = form.data.username,
                                 password = form.data.password,
                                 email = form.data.email,
                                 first_name = form.data.first_name,
                                 last_name = form.data.last_name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("username and email must be unique")
            return render_template("register.html", form=form)
        return redirect("/secret")
        
    return render_template("register.html", form=form)