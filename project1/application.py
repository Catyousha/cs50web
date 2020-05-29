import os

from flask import Flask, session, jsonify, render_template, request, url_for, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt
import requests
import xmltodict
import json

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
    if session.get("user_data") is None:
        return redirect(url_for('login'))
    else:
        return render_template("search.html")

@app.route("/result", methods=['GET'])
def result():
    searchItem = request.args.get("search")
    if searchItem is None:
        return redirect(url_for('index'))

    if type(searchItem) is int:
        books = db.execute("SELECT * FROM books WHERE isbn LIKE :src OR title LIKE :src OR author LIKE :src OR year = :srcInt",{"src": "%"+searchItem+"%", "srcInt": searchItem}).fetchall()
    else:
        books = db.execute("SELECT * FROM books WHERE isbn LIKE :src OR title LIKE :src OR author LIKE :src",{"src": "%"+searchItem+"%"}).fetchall()
    
    return render_template("result.html", books=books)

@app.route("/details/<string:isbn>")
def details(isbn):
    if session.get("user_data") is None:
        return redirect(url_for('login'))
    
    book = db.execute("SELECT * FROM books WHERE isbn = :s", {"s": isbn}).fetchone()
    xml_res = requests.get("https://www.goodreads.com/search/index.xml", params={"key": 'KJ1y2SMO2Tvh7UfI7ldw', "q": isbn})
    data = xmltodict.parse(xml_res.text)
    return render_template("details.html", username = session['user_name'], book=book, data=data['GoodreadsResponse']['search']['results']['work'])

@app.route("/register", methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        checkUser = db.execute("SELECT user_id FROM user_data WHERE username = :username", {"username": username}).rowcount
        if (checkUser>=1):
            return render_template("regist.html", messages="Username has already taken!")
        else:
            pass1 = request.form.get("pass1")
            pass2 = request.form.get("pass2")
            if pass1 != pass2:
                return render_template("regist.html", messages="Password not match!")
            else:
                encpass = sha256_crypt.encrypt(pass1)
                db.execute("INSERT INTO user_data (username, password) VALUES (:username, :password)",{"username":username, "password":encpass})
                db.commit()
                return redirect(url_for("login"))
    else:
        return render_template("regist.html")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        checkUser = db.execute("SELECT user_id FROM user_data WHERE username = :username", {"username": username}).rowcount
        
        if(checkUser != 0):
            password = request.form.get("pass")
            encpass = sha256_crypt.encrypt(password)
            accpass = db.execute("SELECT * FROM user_data WHERE username = :username", {"username": username}).fetchone()
            
            if(sha256_crypt.verify(password, accpass.password)):
                session["user_data"] = accpass.user_id
                session["user_name"] = accpass.username
                return redirect(url_for('index'))
            else:
                return render_template("login.html", messages="Wrong Password!")
        else:
            return render_template("login.html", messages="Username not found!")
    else:
        session["user_data"] = None
        return render_template("login.html")