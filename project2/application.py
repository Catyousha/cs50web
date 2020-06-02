import os
import requests
import random
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
from flask_session import Session


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app)
Session(app)

userList = []

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_dname = request.form.get('displayname')
        if len(user_dname) <=1:
            return render_template("displayname.html", error = "Display name is not valid!") 
        if user_dname in userList:
            return render_template("displayname.html", error = "Display name is already taken!")
        else:
            userList.append(user_dname)
            session['user_dname'] = user_dname
            session['user_color'] = "%06x" % random.randint(0, 0xFFFFFF)
            session.permanent = True
            return redirect(url_for('welcome'))
    else:
        return render_template("displayname.html")

@app.route("/channels")
def channels():
    return render_template("channels.html", viewAs="channel")

@app.route("/create-channel")
def add_channel():
    return render_template("channels.html", viewAs="create")

@app.route("/welcome")
def welcome():
    return render_template("channels.html", viewAs="welcome")

@app.route("/logout")
def logout():
    try:
        userList.remove(session['user_dname'])
    except ValueError:
        pass
    session.clear()
    return redirect(url_for('index'))
