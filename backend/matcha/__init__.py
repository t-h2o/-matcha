from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)


@app.route("/")
def index():
    return "index.html"


@socketio.on("my event")
def test_message(message):
    emit("my response", {"data": message["data"]})


@socketio.on("my broadcast event")
def test_message(message):
    emit("my response", {"data": message["data"]}, broadcast=True)


@socketio.on("connect")
def test_connect():
    emit("my response", {"data": "Connected"})


@socketio.on("disconnect")
def test_disconnect():
    print("Client disconnected")


if __name__ == "__main__":
    socketio.run(app)
