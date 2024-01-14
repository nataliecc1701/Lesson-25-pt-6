
# Library imports
from flask import Flask, render_template, redirect, session, flash
from sqlalchemy.exc import IntegrityError

# Local imports
from models import connect_db, db
# from forms import 
from config import configure_app

app = Flask(__name__)

configure_app(app)
connect_db(app)