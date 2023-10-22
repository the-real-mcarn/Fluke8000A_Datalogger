import serial
import json
import sys
import glob

class F8000A_Serial:
    def __init__(self):
        self.port = None
        self.speed = None
        self.ser = None

        self.connected = False

    def connect(self, port = None, speed = None):
        if port is not None and speed is not None:
            self.port = port
            self.speed = speed

        self.ser = serial.Serial(self.port, self.speed)
        self.connected = True

    def listPorts(self):
        """Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
        """

        if sys.platform.startswith("win"):
            ports = ["COM%s" % (i + 1) for i in range(256)]
        elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob("/dev/tty[A-Za-z]*")
        elif sys.platform.startswith("darwin"):
            ports = glob.glob("/dev/tty.*")
        else:
            raise EnvironmentError("Unsupported platform")
        # return ports

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def read(self, func: callable):
        while self.connected:
            data = self.ser.readline().decode().strip()
            if len(data) > 0:
                res = json.loads(data)
                func(res)

    def disconnect(self):
        self.ser.close()
        self.connected = False
