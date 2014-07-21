import serial

port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=3.0)

port.write("?\r")
rcv = port.read(10)
print(rcv)


