import serial.tools.list_ports

class serialfr:

    def __init__(self):
        self.serialInst = serial.Serial()
        self.serialInst.baudrate = 19200
        for x in serial.tools.list_ports.comports():
            if "Arduino Uno" in x.description:
                self.serialInst.port = x.name
        #self.serialInst.port = "COM5"
        self.serialInst.open()

    def read(self):
        if self.serialInst.in_waiting:
            packet = self.serialInst.readline()
            lst = packet.decode('utf').split(' ')
            return float(lst[0]), float(lst[1]), float(lst[2]), float(lst[3])
        return 0,0,0,0
