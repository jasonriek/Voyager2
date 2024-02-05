import serial
import json
import time

import config
import utils

def serialCall(data={}, delay=0.3):
    '''Makes a serial connection and call to Voyager's hardware.'''
    voyager_serial = None
    response_data = {}
    try:
        voyager_serial = serial.Serial(config.Serial.PORT, config.Serial.BAUD_RATE, timeout=1)
        json_to_send = json.dumps(data)
        voyager_serial.write((json_to_send + '\n').encode('utf-8'))

        # Wait for a moment for the ESP32 to process the request
        time.sleep(delay)
        
        # Read and parse the response from the ESP32
        if voyager_serial.in_waiting > 0:
            line = voyager_serial.readline().decode('utf-8').rstrip()
            try:
                response_data = json.loads(line)
            except json.JSONDecodeError as e:
                response_data = {"Error decoding response JSON:": str(e)}
    
    except Exception as e:
        response_data = {'error':str(e)}
    
    finally:
        # Close the serial connection
        if voyager_serial:
            voyager_serial.close()
    
    return response_data

class Direction:
    STOP = 0
    FORWARD = 1
    BACKWARD = -1
    RIGHT = 2
    LEFT = -2

    @staticmethod
    def parse(direction):
        '''Attempts to read the direction passed from the client, defaults to "Direction.STOP" if failure.'''
        direction = utils.clean(direction)
        directions = {
            '0': Direction.STOP,
            '1': Direction.FORWARD,
            '-1': Direction.BACKWARD,
            'stop': Direction.STOP,
            'freeze': Direction.STOP,
            'pause': Direction.STOP,
            'ahead': Direction.FORWARD,
            'onward': Direction.FORWARD,
            'forward': Direction.FORWARD,
            'backward': Direction.BACKWARD,
            'reverse': Direction.BACKWARD,
            'right': Direction.RIGHT,
            'left': Direction.LEFT,
            'r': Direction.RIGHT,
            'l': Direction.LEFT
        }
        return directions.get(direction, Direction.STOP)

class Command:
    EMERGENCY_STOP = 0
    MOVE = 1
    TURN = 2

    @staticmethod
    def write(command, *args, **kwargs):
        """Formats a command for Voyager's hardware to process."""
        command = {'cmd': command}
        for i, arg in enumerate(args):
            val_key = 'val' + chr(ord('A')+i)
            if i >= ord('Z'):
                raise Exception('Too many arguments are being passed.')
            command[val_key] = arg

        return command