
# Library imports
from flask import Flask, render_template, redirect, session, flash
from sqlalchemy.exc import IntegrityError

# Local imports
from models import connect_db, db, write_data, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from config import configure_app

app = Flask(__name__)

configure_app(app)
connect_db(app)

# Routes
@app.route("/")
def redir_index():
    if "username" in session:
        return redirect(f"/users/{session.username}")
    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register_user():
    if "username" in session:
        return redirect(f"/users/{session.username}")
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
    if "username" in session:
        return redirect(f"/users/{session.username}")
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

@app.route("/users/<username>", methods=["GET", "POST"])
def show_user_info(username):
    if "username" not in session:
        return redirect("/")
    if session["username"] != username:
        return redirect(f"/users/{session['username']}")
    user = User.query.get_or_404(username)
    
    form = FeedbackForm()
    if form.validate_on_submit():
        new_feedback = Feedback(title=form.title.data,
                                content=form.content.data,
                                username=username)
        write_data(new_feedback)
        return redirect(f"/users/{username}")
    
    return render_template("userinfo.html", user=user, form=form)

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    if "username" not in session:
        return redirect("/")
    if session["username"] != username:
        return redirect(f"/users/{session['username']}")
    
    User.query.filter_by(username=username).delete()
    db.session.commit()
    session.pop("username")
    return redirect("/")

@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def edit_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if "username" not in session:
        return redirect("/")
    if session["username"] != feedback.username:
        return redirect(f"/users/{session['username']}")
    
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        write_data(feedback)
        return redirect(f"/users/{feedback.username}")
    return render_template("edit-feedback.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if "username" not in session:
        return redirect("/")
    if session["username"] != feedback.username:
        return redirect(f"/users/{session['username']}")
    
    Feedback.query.filter_by(id=feedback_id).delete()
    db.session.commit()
    return redirect(f"/users/{session['username']}")