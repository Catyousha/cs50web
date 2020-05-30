import os

from flask import Flask, session, jsonify, render_template, request, url_for, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt
import requests
import xmltodict

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["JSON_SORT_KEYS"] = False
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
        books = db.execute("SELECT * FROM books WHERE isbn ILIKE :src OR title ILIKE :src OR author ILIKE :src OR year = :srcInt",{"src": "%"+searchItem+"%", "srcInt": searchItem}).fetchall()
    else:
        books = db.execute("SELECT * FROM books WHERE isbn ILIKE :src OR title ILIKE :src OR author ILIKE :src",{"src": "%"+searchItem+"%"}).fetchall()
    
    return render_template("result.html", books=books)

@app.route("/details/<string:isbn>", methods=['GET','POST'])
def details(isbn):
    if session.get("user_data") is None:
        return redirect(url_for('login'))

    if request.method == 'POST':
        review = request.form.get('reviews')
        rating = request.form.get('rating')
        userid = session['user_data']
        db.execute("INSERT INTO book_reviews (book_isbn, user_id, reviews_text, ratings) VALUES (:b, :u, :r, :s)",{"b": isbn, "u":userid, "r": review, "s":rating})
        db.commit()
        return redirect(url_for('details',isbn=isbn))

    else:
        book = db.execute("SELECT * FROM books WHERE isbn = :s", {"s": isbn}).fetchone()
        reviews = db.execute("SELECT * FROM book_reviews br JOIN user_data ud ON br.user_id = ud.user_id WHERE book_isbn = :b", {"b": isbn}).fetchall()
        canreview = db.execute("SELECT user_id FROM book_reviews WHERE book_isbn = :b AND user_id = :u", {"b": isbn, "u": session['user_data']}).rowcount

        xml_res = requests.get("https://www.goodreads.com/search/index.xml", params={"key": 'KJ1y2SMO2Tvh7UfI7ldw', "q": isbn})
        data = xmltodict.parse(xml_res.text)
        return render_template("details.html", canreview=canreview, reviews=reviews, book=book, data=data['GoodreadsResponse']['search']['results']['work'])

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

@app.route("/api/<string:isbn>")
def books_api(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :s", {"s": isbn}).fetchone()
    review = db.execute("SELECT AVG(ratings) AS rat, COUNT(reviews_text) as count_rev FROM book_reviews WHERE book_isbn = :b", {"b": isbn}).fetchone()
    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "review_count": round(review.count_rev,1),
        "average_score": round(review.rat,1)
    })