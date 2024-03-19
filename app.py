from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import asyncio
import csv

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return '<h1>Test</h1>'

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
