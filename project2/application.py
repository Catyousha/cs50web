import os
import requests
import random
import datetime
from collections import deque
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_session import Session


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app)
Session(app)

channelList = []
userList = []
channelMsg = dict()
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

@app.route("/welcome")
def welcome():
    if session.get('user_dname') is None:
        return redirect(url_for('index'))

    return render_template("channels.html", viewAs="welcome", ch=channelList)

@app.route("/channels/<string:chn>")
def channels(chn):
    if (session.get('user_dname') is None) or (chn not in channelList):
        return redirect(url_for('index'))

    session['current_ch'] = chn
    messages = channelMsg[chn]
    return render_template("channels.html", viewAs="channel", ch=channelList, messages=messages)

@socketio.on("user enter channel", namespace="/")
def enter_channel():
    room = session.get('current_ch')
    join_room(room)
    
    x = datetime.datetime.now()
    timestamp = x.strftime("%b %d, %Y | %X")
    theUser = session['user_dname']
    theColor = session['user_color']
    msg = theUser + " joined the chat"

    message = f"[{timestamp}] <strong style=\"color: #{theColor};\">{msg}</strong>"
    channelMsg[session['current_ch']].append([message])
    
    emit('user join chat',{
        'timestamp': timestamp,
        'user': theUser,
        'color': theColor
    }, room=room)

@socketio.on("user leave channel", namespace="/")
def leave_channel():
    
    x = datetime.datetime.now()
    timestamp = x.strftime("%b %d, %Y | %X")
    theUser = session['user_dname']
    theColor = session['user_color']
    msg = theUser + " leave the chat"

    message = f"[{timestamp}] <strong style=\"color: #{theColor};\">{msg}</strong>"
    channelMsg[session['current_ch']].append([message])
    
    emit('user leave chat',{
        'timestamp': timestamp,
        'user': theUser,
        'color': theColor
    }, room=session.get('current_ch'))
    leave_room(session.get('current_ch'))

@socketio.on("submit message")
def submit_msg(data):
    x = datetime.datetime.now()

    newMsg = data['message-text']
    timestamp = x.strftime("%b %d, %Y | %X")
    channelNow = session['current_ch']
    theUser = session['user_dname']
    theColor = session['user_color']

    if len(channelMsg[channelNow]) > 100:
        channelMsg[channelNow].popleft()

    message = f"[{timestamp}] &lt;<strong style=\"color: #{theColor};\">{theUser}</strong>&gt; {newMsg}"
    channelMsg[channelNow].append([message])

    emit('put message', {
        'user': theUser,
        'color': theColor,
        'timestamp': timestamp,
        'msg': newMsg},
        room=channelNow)

@app.route("/create-channel", methods=['POST','GET'])
def add_channel():
    if session.get('user_dname') is None:
        return redirect(url_for('index'))

    session['current_ch'] = None
    return render_template("channels.html", viewAs="create", ch=channelList)

@socketio.on("submit new channel")
def submit_newch(data):
    newCh = data['newchannel-name']
    
    if newCh in channelList:
        emit("error add channel",{
            "error": "Channel is already exist!"
        });
    elif len(newCh) <=1:
        emit("error add channel",{
            "error": "Channel name is not valid!"
        });
    else:
        channelList.append(newCh)
        channelMsg[newCh] = deque()

        emit("new channel added", {
            "newch": newCh
        }, broadcast=True)


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
