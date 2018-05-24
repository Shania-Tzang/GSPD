import serial
import streamer_better as streamer
import threading
import time

streamer = streamer.Streamer()

# Establish serial connection to the Arduino
arduino_ser = serial.Serial('/dev/tty.team1ARDUINO-DevB')

# Establish serial connection to the EV3
#ev3_ser = serial.Serial('/dev/tty.ev3dev')

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

class StreamerThread(object):
    
    def __init__(self, interval=1):
        self.interval = interval
        
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = False
        thread.start()

    def run(self):
        #while True:
            #print('\nRunning streamer.py...\n\n')
            streamer.run()
            time.sleep(self.interval)

def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True

def translate_path(x, y):
    return str(y) + str(x)

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
    if (vis >= vis_req[0] and vis <= vis_req[1]) or (vis_req[0] == 0.0 and vis_req[1] == 0.0):
        no_of_reqs_fulfilled += 1
    if (ir >= ir_req[0] and ir <= ir_req[1]) or (ir_req[0] == 0.0 and ir_req[1] == 0.0):
        no_of_reqs_fulfilled += 1
    if (no_of_reqs_fulfilled == 4):
        return True
    else:
        return False

def read_sensor_values():
    print("Retrieving sensor data...\n")
    
    while(streamer.is_waiting == False): time.sleep(0.1)

    streamer.stream_is_busy = True

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

    streamer.stream_is_busy = False

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
    min_hum = input("Enter (1) Humidity requirement (min): ")
    max_hum = input("Enter (1) Humidity requirement (max): ")

    if (is_number(min_hum) and is_number(max_hum)):
        humidity_req = [float(min_hum), float(max_hum)]
    else:
        humidity_req = [0.0, 0.0]
    min_temp = input("\nEnter (2) Temperature requirement (min): ")
    max_temp = input("Enter (2) Temperature requirement (max): ")
    
    if (is_number(min_temp) and is_number(max_temp)):
        temperature_req = [float(min_temp), float(max_temp)]
    else:
        temperature_req = [0.0, 0.0]

    min_vis = input("\nEnter (3) Visible light requirement (min): ")
    max_vis = input("Enter (3) Visible light requirement (max): ")

    if (is_number(min_vis) and is_number(max_vis)):
        vis_req = [float(min_vis), float(max_vis)]
    else:
        vis_req = [0.0, 0.0]

    min_ir = input("\nEnter (4) IR requirement (min): ")
    max_ir = input("Enter (4) IR requirement (max): ")

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
        print("Moving package to storage destination: " + str(arduino_pos) + "\n\n")
        translated_path = translate_path(arduino_pos[0], arduino_pos[1])
        #streamer.run()
        print(translated_path)
        ev3_ser.write(translated_path)
    else:
        print("Requirements not fulfilled.")
        print("Moving package to another destination. " + str(alt_pos) + "\n\n")
        translated_path = translate_path(alt_pos[0], alt_pos[1])
        #streamer.run()
        print(translated_path)
        ev3_ser.write(translated_path)

streamer_thread = StreamerThread()

while True:
    run_menu()
