import serial
import time

ser = serial.Serial('/dev/tty.ev3dev-SerialPort')

msg = raw_input("how many lines to pass?")
ser.write(msg)
time.sleep(2)

while(True):
    reSend = raw_input("send again? y/n")
    if reSend == "y":
        ser.write(msg)
