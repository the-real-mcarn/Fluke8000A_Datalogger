import serial

# Replace 'COM7' with the name of your serial port
ser = serial.Serial('COM7', 9600)

while True:
    # Read a line of data from the serial port
    data = ser.readline().decode().strip()
    
    # Print the data to the console
    print(data)
