# python Imports

from flask import Flask, render_template, session, flash, request, redirect, url_for
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_socketio import SocketIO, emit

app = Flask(__name__)

# secret Key

app.secret_key = "Po37#itOp"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
socketio = SocketIO(app)


# Models

# User Model

class User(db.Model):

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    bio = db.Column(db.String(300), nullable=True)


# Post Model

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    likes = db.Column(db.Integer, default=0)

    user = db.relationship("User", backref="posts")


# Message Model

class Message(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.Text, nullable=False)

    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ERROR FIX:
    # Message has two foreign keys pointing to User,
    # so sender and receiver relationships must be specified separately.

    sender = db.relationship("User", foreign_keys=[sender_id])
    receiver = db.relationship("User", foreign_keys=[receiver_id])


with app.app_context():
    db.create_all()


# URL Routing


# Login page

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["UsernameL"]
        password = request.form["PasswordL"]

        user = User.query.filter_by(username=username).first()

        if user and password == user.password:

            session["user_id"] = user.id
            return render_template("index.html")

        else:
            flash("Invalid username or password")

    return render_template("login.html")


# Sign up Page

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["UsernameS"]
        password = request.form["PasswordS"]

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:

            flash("User already exists. Please Login")
            return render_template("signup.html")

        new_user = User(
            username=username,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully You can login now.")

        return render_template("signup.html")

    return render_template("signup.html")


# index page

@app.route("/index")
def index():

    posts = Post.query.order_by(Post.created_at.desc()).all()

    return render_template("index.html", posts=posts)


# Creating a Post

@app.route("/createpost", methods=["GET", "POST"])
def createpost():

    if request.method == "POST":

        post_text = request.form["PostText"]

        # Post object create

        post = Post(
            content=post_text,
            user_id=session["user_id"]
        )

        db.session.add(post)
        db.session.commit()

        flash("Post created succesfully")

    return render_template("createpost.html")


# Profile page

@app.route("/profile/<int:user_id>")
def profile(user_id):

    user = User.query.get_or_404(user_id)

    posts = Post.query.filter_by(
        user_id=user.id
    ).order_by(
        Post.created_at.desc()
    ).all()

    return render_template(
        "profile.html",
        user=user,
        posts=posts
    )


# Messages page

@app.route("/messages")
def messages():

    current_user_id = session["user_id"]

    messages = Message.query.filter(
        (Message.sender_id == current_user_id) |
        (Message.receiver_id == current_user_id)
    ).order_by(
        Message.created_at.desc()
    ).all()

    return render_template(
        "messages.html",
        messages=messages
    )


# Chats page

@app.route("/messages/<int:user_id>")
def chat(user_id):

    current_user_id = session["user_id"]

    messages = Message.query.filter(
        (
            (Message.sender_id == current_user_id) &
            (Message.receiver_id == user_id)
        )
        |
        (
            (Message.sender_id == user_id) &
            (Message.receiver_id == current_user_id)
        )
    ).order_by(
        Message.created_at.asc()
    ).all()

    user = User.query.get_or_404(user_id)

    return render_template(
        "chat.html",
        user=user,
        messages=messages
    )


# Web Socket

@socketio.on("send_message")
def handle_message(data):

    current_user_id = session["user_id"]

    receiver_id = data["receiver_id"]
    message_text = data["message"]

    # Save message into database

    new_message = Message(
        content=message_text,
        sender_id=current_user_id,
        receiver_id=receiver_id
    )

    db.session.add(new_message)
    db.session.commit()

    # Send message back to connected users

    emit(
        "receive_message",
        {
            "sender": new_message.sender.username,
            "message": new_message.content,
            "created_at": str(new_message.created_at)
        },
        broadcast=True
    )


# admin page

@app.route("/admin")
def admin():

    users = User.query.all()

    return render_template("admin.html", users=users)


if __name__ == "__main__":

    socketio.run(
        app,
        debug=True,
        port=8000
    )