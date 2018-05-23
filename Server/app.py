import serial

# Establish serial connection to the Arduino
arduino_ser = serial.Serial('/dev/tty.team1ARDUINO-DevB')

# Establish serial connection to the EV3
ev3_ser = serial.Serial('/dev/tty.ev3dev')

# Coords #########################
arduino_pos = (3, 3)
alt_pos = (3, 1)
##################################

# Variables for sensor values ####
humidity = 0.0
temperature = 0.0
vis = 0.0
ir = 0.0
##################################

def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True

def translate_path((x, y)):
    new_x = x-1
    new_x_string = str(new_x)
    new_y = y-1
    new_y_string = str(new_y)
    translated_path = new_y_string + new_x_string
    return translated_path

def req_are_fulfilled(values, humidity_req, temperature_req, vis_req, ir_req):
    no_of_reqs_fulfilled = 0
    
    humidity = values[0]
    temperature = values[1]
    vis = values[2]
    ir = values[3]
    
    if (humidity >= humidity_req[0] and humidity <= humidity_req[1]) or (humidity_req[0] == 0.0 and humidity_req[1] == 0.0):
        no_of_reqs_fulfilled += 1
    if (temperature >= temperature_req[0] and temperature <= temperature_req[1]) or (temperature_req[0] == 0.0 and temperature_req[1] == 0.0):
        no_of_reqs_fulfilled += 1
    if (vis >= humidity_req[0] and vis <= humidity_req[1]) or (humidity_req[0] == 0.0 and humidity_req[1] == 0.0):
        no_of_reqs_fulfilled += 1
    if (ir >= ir_req[0] and ir <= ir_req[1]) or (ir_req[0] == 0.0 and ir_req[1] == 0.0):
        no_of_reqs_fulfilled += 1
    if (no_of_reqs_fulfilled == 4):
        return True
    else:
        return False

def read_sensor_values():
    print("Retrieving sensor data...\n")
    
    values = []
    string = arduino_ser.readline()
    
    for t in string.split():
        try:
            values.append(float(t))
        except ValueError:
            pass

    humidity = values[0]
    temperature = values[1]
    vis = values[2]
    ir = values[3]

    print("=== CURRENT SENSOR DATA ========================")
    print("Humidity:\t\t\t" + str(humidity).strip('\n'))
    print("Temperature:\t\t\t" + str(temperature).strip('\n'))
    print("Vis:\t\t\t\t" + str(vis).strip('\n'))
    print("IR:\t\t\t\t" + str(ir).strip('\n'))
    print("================================================\n\n")

    return values

def run_menu():
    humidity_req = [0.0, 0.0]
    temperature_req = [0.0, 0.0]
    vis_req = [0.0, 0.0]
    ir_req = [0.0, 0.0]
    
    print("\n=== WELCOME! ===================================")
    print("Please set the requirements for the package.\n")
    print("All inputs must be numbers and a valid range,")
    print("else (0.0, 0.0) will be set.\n\n")
    min_hum = raw_input("Enter (1) Humidity requirement (min): ")
    max_hum = raw_input("Enter (1) Humidity requirement (max): ")

    if (is_number(min_hum) and is_number(max_hum)):
        humidity_req = [float(min_hum), float(max_hum)]
    else:
        humidity_req = [0.0, 0.0]
    min_temp = raw_input("\nEnter (2) Temperature requirement (min): ")
    max_temp = raw_input("Enter (2) Temperature requirement (max): ")
    
    if (is_number(min_temp) and is_number(max_temp)):
        temperature_req = [float(min_temp), float(max_temp)]
    else:
        temperature_req = [0.0, 0.0]

    min_vis = raw_input("\nEnter (3) Visible light requirement (min): ")
    max_vis = raw_input("Enter (3) Visible light requirement (max): ")

    if (is_number(min_vis) and is_number(max_vis)):
        vis_req = [float(min_vis), float(max_vis)]
    else:
        vis_req = [0.0, 0.0]

    min_ir = raw_input("\nEnter (4) IR requirement (min): ")
    max_ir = raw_input("Enter (4) IR requirement (max): ")

    if (is_number(min_ir) and is_number(max_ir)):
        ir_req = [float(min_ir), float(max_ir)]
    else:
        ir_req = [0.0, 0.0]

    print("\n=== PACKAGE REQUIREMENTS =======================")
    print("Humidity (min, max):\t\t" + "(" + str(humidity_req[0]) + ", " + str(humidity_req[1]) + ")")
    print("Temperature (min, max):\t\t" + "(" + str(temperature_req[0]) + ", " + str(temperature_req[1]) + ")")
    print("Visible light (min, max):\t" + "(" + str(vis_req[0]) + ", " + str(vis_req[1]) + ")")
    print("IR (min, max):\t\t\t" + "(" + str(ir_req[0]) + ", " + str(ir_req[1]) + ")")
    print("================================================\n")

    values = read_sensor_values()

    if req_are_fulfilled(values, humidity_req, temperature_req, vis_req, ir_req):
        print("All requirements fulfilled!")
        print("Moving package to storage destination.")
        translated_path = translate_path(arduino_pos)
        ev3_ser.write(translated_path)
    else:
        print("Requirements not fulfilled.")
        print("Moving package to another destination.")
        translated_path = translate_path(alt_pos)
        ev3_ser.write(translated_path)

run_menu()
