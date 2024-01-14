from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect the app to the database"""
    
    db.app = app
    db.init_app(app)

# Models follow
class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(20), primary_key = True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)
    
    
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register a user and store a salted hash of their password"""
        
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")
        
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Authenticate a user by username and password
        
        Returns the user if valid, else returns False"""
        
        u = cls.query.filter_by(username=username).first()
        
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False