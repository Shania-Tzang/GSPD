import serial

# Establish serial connection to the Arduino
ser = serial.Serial('/dev/tty.team1ARDUINO-DevB')

values = []

# Variables for sensor values
humidity = 0.0
temperature = 0.0
vis = 0.0
ir = 0.0

while True:
    string = ser.readline()
    
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

    print("=== DATA ==============")
    print("Humidity: " + str(humidity).strip('\n'))
    print("Temperature: " + str(temperature).strip('\n'))
    print("Vis: " + str(vis).strip('\n'))
    print("IR: " + str(ir).strip('\n'))
    print("=======================\n\n")

