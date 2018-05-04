import serial

# Establish serial connection to the Arduino
ser = serial.Serial('/dev/tty.team1ARDUINO-DevB')

# Variables for sensor values
humidity = 0.0
humidity_str = "0.0"

temperature = 0.0
temperature_str = "0.0"

vis = 0.0
vis_str = "0.0"

ir = 0.0
ir_str = "0.0"

while True:
    #print(ser.readline())
    s = ser.readline()

    if ':' in s:
        if 'Humidity' in s:
            humidity_data = s.split(": ",1)[1]
            humidity_str = str(humidity_data).strip('\n')
            humidity = humidity_data
        if 'Temperature' in s:
            temperature_data = s.split(": ",1)[1]
            temperature_str = str(temperature_data).strip('\n')
            temperature = temperature_data
        if 'Vis' in s:
            vis_data = s.split(": ",1)[1]
            vis_str = str(vis_data).strip('\n')
            vis = vis_data
        if 'IR' in s:
            ir_data = s.split(": ",1)[1]
            ir_str = str(ir_data).strip('\n')
            ir = ir_data

    print("=== DATA ==============")
    print("Humidity: " + humidity_str)
    print("Temperature: " + temperature_str)
    print("Vis: " + vis_str)
    print("IR: " + ir_str)
    print("=======================\n\n")

