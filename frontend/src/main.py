import serial
import json

# Replace 'COM7' with the name of your serial port
ser = serial.Serial('COM10', 9600)

try:
    while True:
        # Read a line of data from the serial port
        data = ser.readline().decode().strip()
    
        # Print the data to the console
        res = json.loads(data)
        
        print(F"Value: {res['digits']}")
        
        if res['polarity'] == 1: 
            print("Polarity: Positive")
        else:
            print("Polarity: Negative")
            
        if res['overload'] == 1:
            print("Overload warning!")
except KeyboardInterrupt:
    ser.close()
    exit()