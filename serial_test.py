import serial
import json
import time

ser = serial.Serial('/dev/ttyAMA0', 1000000)

while True:
    data_to_send = {
        "sensor": "Raspberry Pi",
        "value": 42
    }
    json_to_send = json.dumps(data_to_send)
    
    ser.write((json_to_send + '\n').encode('utf-8'))
    
    # Wait for a moment before sending the next JSON
    time.sleep(1)
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        try:
            response_data = json.loads(line)
            print("Received acknowledgment:", response_data["message"])
        except json.JSONDecodeError as e:
            print(f"Error decoding acknowledgment: {e}")