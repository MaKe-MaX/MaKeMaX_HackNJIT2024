import serial.tools.list_ports

class serialfr:

    def __init__(self):
        self.serialInst = serial.Serial()
        self.serialInst.baudrate = 19200
        self.serialInst.port = "COM3"
        self.serialInst.open()

    def read(self):
        if self.serialInst.in_waiting:
            packet = self.serialInst.readline()
            lst = packet.decode('utf').split(' ')
            return float(lst[0]), float(lst[1]), float(lst[2]), float(lst[3])
        return 0,0,0,0
