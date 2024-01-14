
# Library imports
from flask import Flask, render_template, redirect, session, flash
from sqlalchemy.exc import IntegrityError

# Local imports
from models import connect_db, db
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
    return render_template("register.html", form=form)