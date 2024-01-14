from app import app
from models import db, User, Feedback

app.app_context().push()

db.drop_all()
db.create_all()

users = [
    User.register("StevieChicks", "ChickensRc00l", "steviechicks@springboard.com", "Stevie", "Chicks"),
    User.register("NinthSaint", "IhttTss4ever", "harrowharkthefirst@mithraeum.gov", "Harrowhark", "Nonagesimus"),
]

users[1].is_admin = True

db.session.add_all(users)
db.session.commit()

feedback = [
    Feedback(title="I have always lived", content="I have never been murdered before and I truly don't intend to start now", username="NinthSaint"),
    Feedback(title="Bock Bock", content="cluck!", username="StevieChicks"),
]

db.session.add_all(feedback)
db.session.commit()