from flask import Flask, jsonify, render_template
from flask_restful import Resource, Api, marshal_with
from flask_socketio import SocketIO, emit, send
from threading import Thread
import time
from calculations import *
from flask_cors import CORS
from flask import requestE
from calculations import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')
thread = None
clients = 0
CORS(app)

def ini_socket():
    global clients, thread
    thread = None


@app.route('/api/socket')
def index():
    print('Route socket init')
    global thread
    if thread is None:
        thread = Thread(target=ini_socket)
        thread.start()
    return ('{"ok":"success"}')


# Function that runs when a clients get connected to the server
@socketio.on('connect')
def test_connect():
    global clients
    clients += 1
    print('Client connected test')


# Read data from client
@socketio.on('new-message')
def handle_message(message):
    print('received message' + message)
    send_data()


# Send data to client
@socketio.on('new-message-s')
def send_data():
    emit('data-msg', {'message': 'message'})


@socketio.on('disconnect')
def test_disconnect():
    global clients
    clients -= 1
    print('Client disconnected')

@app.route('/table1', methods=['POST'])

def update_risks_table():
    new_json = request.data
    if BaseClass.risks_table.read_from_json(new_json, table_name='risks'):
        return 'All good', 200
    else:
        return 'Error', 500

@app.route('/table2', methods=['POST'])
def update_costs_table():
    new_json = request.data
    if BaseClass.costs_table.read_from_json(new_json, table_name='risks'):
        return 'All good', 200
    else:
        return 'Error', 500

@app.route('/table3', methods=['POST'])
def update_reasoning_table():
    new_json = request.data
    if BaseClass.risks_table.read_from_json(new_json, table_name='reasoning'):
        return 'All good', 200
    else:
        return 'Error', 500

@app.route('/table1', methods=['GET'])
def send_table_with_risks():
    response = jsonify(BaseClass.risks_table.convert_numpy_to_json())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/table2', methods=['GET'])
def send_table2_with_risks():
    response = jsonify(BaseClass.costs_table.convert_numpy_to_json())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/table3', methods=['GET'])
def send_table3_with_risks():
    response = jsonify(BaseClass.reasons_table.convert_numpy_to_json())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


# This is the function that will create the Server in the ip host and port 5000
if __name__ == "__main__":
    print("starting webservice")
    app.run()
