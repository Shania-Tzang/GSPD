import serial

# Establish serial connection to the Arduino
arduino_ser = serial.Serial('/dev/tty.team1ARDUINO-DevB')

# Establish serial connection to the EV3
ev3_ser = serial.Serial('/dev/tty.ev3dev')

values = []
path = [0, 1337]

# Variables for sensor values
humidity = 0.0
temperature = 0.0
vis = 0.0
ir = 0.0

string = arduino_ser.readline()

for t in string.split():
    try:
        values.append(float(t))
    except ValueError:
        pass

print(values)

humidity = values[0]
temperature = values[1]
vis = values[2]
ir = values[3]

# TODO: Path --->
ev3_ser.write(path[0])
ev3_ser.write(path[1])
