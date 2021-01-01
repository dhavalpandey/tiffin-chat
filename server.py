from flask import Flask, redirect, url_for, render_template, request
from flask_socketio import SocketIO, join_room

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/join")
def joinRoom():
    return render_template("join.html")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/chat")
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template("chat.html", username=username, room=room)
    else: 
        return redirect(url_for('home'))

#my requirements
"""
flask
flask-socketio
eventlet
"""

#404
@app.route("/<url>")
def user(url):
    return f"The web-page you requested for <a href='https://tiffin-chat.herokuapp.com/{url}'>(dhaval-blog.herokuapp.com/{url})</a> is not avalibale at the moment! Error code: 404. "

@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('send_message')
def handle_send_message_event(data):
     app.logger.info("{} has sent a message to the room {}".format(data['username'], data['room'], data['message']))
     socketio.emit('receive_message', data, room=data['room'])

if __name__ == "__main__":
    socketio.run(app, debug=True)