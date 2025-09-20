import eventlet
import eventlet.wsgi
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room

from consts import ROOM, SECRET_KEY, PORT, CERTFILE, KEYFILE

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('join')
def on_join(data):
    join_room(ROOM)
    print(f"{data['username']} joined")


@socketio.on('media')
def on_media(data, *args):
    emit('media', data, room=ROOM, include_self=False, binary=True)


@socketio.on('audio')
def on_audio(data, *args):
    emit('audio', data, room=ROOM, include_self=False, binary=True)


if __name__ == '__main__':
    if CERTFILE and KEYFILE:
        ssl_context = eventlet.wrap_ssl(eventlet.listen(('0.0.0.0', PORT)),
                                        certfile=CERTFILE,
                                        keyfile=KEYFILE,
                                        server_side=True)
        print(f"Server running on https://0.0.0.0:{PORT}")
        eventlet.wsgi.server(ssl_context, app)
    else:
        print(f"Server running on http://0.0.0.0:{PORT}")
        socketio.run(app, host='0.0.0.0', port=PORT)
        