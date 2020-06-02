import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("displayname.html")

@app.route("/channels")
def channels():
    return render_template("channels.html")

@app.route("/create-channel")
def add_channel():
    return render_template("createchannel.html")