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

channelList = []
userList = []

#for emitting purposes
emit_data = dict()

@app.route("/", methods=['GET', 'POST'])
def index():
    if session.get('user_dname') is not None:
        return redirect(url_for('welcome'))

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

@app.route("/channels/<string:chn>")
def channels(chn):
    if session.get('user_dname') is None:
        return redirect(url_for('index'))
    
    session['current_ch'] = chn
    return render_template("channels.html", viewAs="channel", ch=channelList)

@app.route("/create-channel", methods=['POST','GET'])
def add_channel():
    if session.get('user_dname') is None:
        return redirect(url_for('index'))
        
    session['current_ch'] = []
    return render_template("channels.html", viewAs="create", ch=channelList)

@socketio.on("submit new channel")
def submit_newch(data):
    newCh = data['newchannel-name']
    if newCh in channelList:
        return render_template("channels.html", viewAs="create", ch=channelList, error="Channel is already exist!")
    elif len(newCh) <=1:
        return render_template("channels.html", viewAs="create", ch=channelList, error="Channel name is not valid!")
    else:
        channelList.append(newCh)
        emit_data['newch'] = newCh
        emit("new channel added", emit_data, broadcast=True)

@app.route("/welcome")
def welcome():
    if session.get('user_dname') is None:
        return redirect(url_for('index'))

    return render_template("channels.html", viewAs="welcome", ch=channelList)

@app.route("/logout")
def logout():
    if session.get('user_dname') is None:
        return redirect(url_for('index'))        
    try:
        userList.remove(session['user_dname'])
    except ValueError:
        pass
    session.clear()
    return redirect(url_for('index'))
