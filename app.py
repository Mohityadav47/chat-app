from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

chat_history = []  # Simple in-memory chat storage

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    # जब कोई user connect हो, उसे पुराना chat भेजो
    for msg in chat_history:
        send(msg)

@socketio.on('message')
def handle_message(data):
    print(f"{data['user']}: {data['text']}")
    message = {'user': data['user'], 'text': data['text']}
    chat_history.append(message)  # Save in memory
    send(message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
