from flask import Flask, render_template, jsonify

from voyager_communication import serialCall, Command, Direction

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'Message': 'Welcome to Voyager!'})

@app.route('/stop')
def stop():
    return jsonify(serialCall(Command.write(Command.EMERGENCY_STOP)))

@app.route('/move/<direction>', methods=['GET'])
def move(direction):
    direction = Direction.parse(direction)
    return jsonify(serialCall(Command.write(Command.MOVE, direction, direction)))

@app.route('/turn/<direction>', methods=['GET'])
def turn(direction):
    direction = Direction.parse(direction)
    command = {}
    if direction > 0: # Turn right
        command = Command.write(Command.TURN, 1, -1)
    else:             # Turn left
        command = Command.write(Command.TURN, -1, 1) 
    return jsonify(serialCall(command))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)