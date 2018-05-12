import serial

# Establish serial connection to the Arduino
ser = serial.Serial('/dev/tty.team1ARDUINO-DevB')

# Variables for sensor values
humidity = 0.0
temperature = 0.0
vis = 0.0
ir = 0.0

while True:
    if (humidity == 0.0 or temperature == 0.0 or vis == 0.0 or ir == 0.0):
        s = ser.readline()

        print(s)
        if ':' in s:
            if 'Humidity' in s:
                humidity_data = s.split(": ",1)[1]
                print(humidity_data)
                humidity = humidity_data
            if 'Temperature' in s:
                temperature_data = s.split(": ",1)[1]
                temperature = temperature_data
            if 'Vis' in s:
                vis_data = s.split(": ",1)[1]
                vis = vis_data
            if 'IR' in s:
                ir_data = s.split(": ",1)[1]
                ir = ir_data
    else:
        break

print("test\n")
print(humidity)
print("test\n")
print(temperature)
print("test\n")
print(vis)
print("test\n")
print(ir)
