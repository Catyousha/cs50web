import os

from flask import Flask, session, render_template, request, url_for, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt
import requests

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=['GET','POST'])
def index():
    if request.method != 'POST' or session.get("user_data") is None:
        return redirect(url_for('login'))
    else:
        return render_template("search.html")

@app.route("/register", methods = ['POST', 'GET'])
def register():
    return render_template("regist.html")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        checkUser = db.execute("SELECT user_id FROM user_data WHERE username = :username", {"username": username}).rowcount
        
        if(checkUser != 0):
            password = request.form.get("pass")
            encpass = sha256_crypt.encrypt(password)
            accpass = db.execute("SELECT password FROM user_data WHERE username = :username", {"username": username}).fetchone()
            
            if(sha256_crypt.verify(encpass, accpass.password)):
                return redirect(url_for('index'))
            else:
                return render_template("login.html", messages= "Wrong Password!")
        else:
            return render_template("login.html", messages="Username not found!")
    else:
        return render_template("login.html")