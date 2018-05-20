import serial

# Establish serial connection to the Arduino
#arduino_ser = serial.Serial('/dev/tty.team1ARDUINO-DevB')

# Establish serial connection to the EV3
#ev3_ser = serial.Serial('/dev/tty.ev3dev')

values = []
path = [0, 1337]

# Variables for sensor values
humidity = 0.0
temperature = 0.0
vis = 0.0
ir = 0.0

def translate_path((x, y)):
    new_x = x-1
    new_x_string = str(new_x)
    new_y = y-1
    new_y_string = str(new_y)
    translated_path = new_y_string + new_x_string
    return translated_path

# Decide target coordinates based on sensor values ...
# ......
# Example output: (4, 3)

translated_path = translate_path((4, 3))

ev3_ser.write(translated_path)






"""string = arduino_ser.readline()
    
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
    """
