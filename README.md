# Postit-

Hey there guys, this is website named Postit! in this website user can write text based post inspired by twitter and you can chat here with other users with there user id i have used Flask,Sqlite ,Socket.IO,HTML,CSS and Javascript.


* User Signup & Login
* User Profiles
* reate and delete posts
* Like posts
* omment on posts
* Real-time messaging with Flask-SocketIO
* Session-based authentication
* Flask-SQLAlchemy database integration
* Responsive frontend

# Tech Stack

# For backend

* Python
* Flask
* Flask-SQLAlchemy
* Flask-SocketIO

# For Database

* SQLite

# For Frontend

* HTML5
* CSS3
* JavaScript

## Project Structure

Postit/
│
├── app.py
├── users.db
│
├── templates/
│   ├── login.html
│   ├── signup.html
│   ├── profile.html
│   ├── messages.html
│   ├── create_post.html
│   └── ...
│
├── static/
│   └── style.css
│
└── README.md

#Installation

# 1. Clone the repository

git clone https://github.com/yourusername/postit.git
cd postit


### 2. Create a virtual environment

bash
python -m venv venv

Activate it:

**Linux/macOS**
bash

source venv/bin/activate


**Windows**

bash
venv\Scripts\activate
```

### 3. Install dependencies

bash
pip install -r requirements.txt

### 4. Run the application

bash
python app.py


The application will be available at:

http://127.0.0.1:8000

##  Authentication

Postit uses Flask sessions for user authentication.

## Real-Time Messaging

The messaging system uses Flask-SocketIO which is flask web sockets plugin for real-time communication between users without requiring a traditional page refresh for every message.

##  Database

Postit currently uses SQLite with Flask-SQLAlchemy for database management.

The database stores information such as:

* Users
* Posts
* Likes
* Comments
* Messages
* User profiles

## 🔮 Future Improvements

* Follow/unfollow system
* werkzueg security for password hashing
* Notifications
* Search functionality
* Better messaging UI
* PostgreSQL support for production
* Improved authorization and admin controls by Flask-Admin
* Deployment with a production WSGI server

## 📚 What I Learned

While building Postit, I practiced:

* Flask application structure
* Authentication and sessions
* Password hashing
* SQLAlchemy relationships
* CRUD operations
* Database design
* User authorization
* Real-time communication with SocketIO
* Frontend-backend integration
* Git and GitHub workflow

Project BY :-

Roopnarayan

Built as a learning project to strengthen my Python, Flask, backend development, databases, and real-time web application skills.

you can check use it and have fun ! Will try to deploy it soon if some of guys like it to be deployed.

