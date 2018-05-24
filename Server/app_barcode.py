import serial
import sys

# Based on: https://plot.ly/raspberry-pi/tmp36-temperature-tutorial/
# Plotly library
import plotly.plotly as py
import plotly.graph_objs as go
import json  # used to parse config.json

from os.path import abspath, dirname, join

json_path = join(dirname(abspath(__file__)), 'config.json')

# Parse the configuration
with open(json_path) as config_file:
	plotly_user_config = json.load(config_file)

# Sign in to plotly
py.sign_in(
	plotly_user_config["plotly_username"],
	plotly_user_config["plotly_api_key"]
)

stream_id = plotly_user_config['plotly_streaming_tokens'][4]

stream_config = go.Stream(token=stream_id, maxpoints=1)

data = [go.Scatter(
	x=[0.5], y=[0.5], stream=stream_config,
	marker=dict(
		size=60,
		color='rgba(152, 0, 0, .8)',
		line=dict(
			width=2,
			color='rgb(0, 0, 0)'
		)
	))]
layout = go.Layout(
	# dragmode='select',
	xaxis=dict(
		range=[0, 3],
		dtick=1,
		fixedrange=True,
		# Styling
		showgrid=True,
		zeroline=True,
		showline=True,
		mirror='ticks',
		gridcolor='#bdbdbd',
		gridwidth=4,
		zerolinecolor='#969696',
		zerolinewidth=4,
		linecolor='#636363',
		linewidth=4
	),
	yaxis=dict(
		range=[0, 3],
		dtick=1,
		fixedrange=True,
		# Styling again
		showgrid=True,
		zeroline=True,
		showline=True,
		mirror='ticks',
		gridcolor='#bdbdbd',
		gridwidth=4,
		zerolinecolor='#969696',
		zerolinewidth=4,
		linecolor='#636363',
		linewidth=4
	)
)

fig = go.Figure(data=data, layout=layout)
url1 = py.plot(
	fig, filename='Robot position',
	fileopt='overwrite', auto_open=False
)

print("View your graph here: {}".format(url1))

stream = py.Stream(stream_id)
stream.open()


# Establish serial connection to the Arduino
arduino_ser = serial.Serial('/dev/tty.team1ARDUINO-DevB')

# Establish serial connection to the EV3
ev3_ser = serial.Serial('/dev/tty.ev3dev-SerialPort')

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

def translate_path(x, y):
	return (str(y) + str(x))

def req_are_fulfilled(values, humidity_req, temperature_req, vis_req, ir_req):
	no_of_reqs_fulfilled = 0

	humidity = values[0]
	temperature = values[1]
	vis = values[2]
	ir = values[3]

	print("CHECK: VALUES")
	print(humidity)
	print(temperature)
	print(vis)
	print(ir)
	print("CHECK: REQ VALUES")
	print(humidity_req)
	print(temperature_req)
	print(vis_req)
	print(ir_req)

	if (humidity >= humidity_req[0] and humidity <= humidity_req[1]) or (humidity_req[0] == 0.0 and humidity_req[1] == 0.0):
		no_of_reqs_fulfilled += 1
		print("humidity OK")
	if (temperature >= temperature_req[0] and temperature <= temperature_req[1]) or (temperature_req[0] == 0.0 and temperature_req[1] == 0.0):
		no_of_reqs_fulfilled += 1
		print("temperature OK")
	if (vis >= vis_req[0] and vis <= vis_req[1]) or (vis_req[0] == 0.0 and vis_req[1] == 0.0):
		no_of_reqs_fulfilled += 1
		print("vis OK")
	if (ir >= ir_req[0] and ir <= ir_req[1]) or (ir_req[0] == 0.0 and ir_req[1] == 0.0):
		no_of_reqs_fulfilled += 1
		print("ir OK")
	if (no_of_reqs_fulfilled == 4):
		return True
	else:
		return False

def read_sensor_values():
	print("Retrieving sensor data...\n")

	values = []
	string = arduino_ser.readline().decode().strip()


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
	print("block")
	package_requirements = ev3_ser.readline().decode().split("_")
	print("done")
	global rec
	humidity_req = [0.0, 0.0]
	temperature_req = [0.0, 0.0]
	vis_req = [0.0, 0.0]
	ir_req = [0.0, 0.0]

	#print("\n=== WELCOME! ===================================")
	#print("Please set the requirements for the package.\n")
	#print("All inputs must be numbers and a valid range,")
	#print("else (0.0, 0.0) will be set.\n\n")
	#min_hum = input("Enter (1) Humidity requirement (min): ")
	#max_hum = input("Enter (1) Humidity requirement (max): ")

	min_hum = package_requirements[0]
	max_hum = package_requirements[1]

	if (is_number(min_hum) and is_number(max_hum)):
		humidity_req = [float(min_hum), float(max_hum)]
	else:
		humidity_req = [0.0, 0.0]
	#min_temp = input("\nEnter (2) Temperature requirement (min): ")
	#max_temp = input("Enter (2) Temperature requirement (max): ")

	min_temp = package_requirements[2]
	max_temp = package_requirements[3]

	if (is_number(min_temp) and is_number(max_temp)):
		temperature_req = [float(min_temp), float(max_temp)]
	else:
		temperature_req = [0.0, 0.0]

	#min_vis = input("\nEnter (3) Visible light requirement (min): ")
	#max_vis = input("Enter (3) Visible light requirement (max): ")

	min_vis = package_requirements[4]
	max_vis = package_requirements[5]

	if (is_number(min_vis) and is_number(max_vis)):
		vis_req = [float(min_vis), float(max_vis)]
	else:
		vis_req = [0.0, 0.0]

	#min_ir = input("\nEnter (4) IR requirement (min): ")
	#max_ir = input("Enter (4) IR requirement (max): ")

	min_ir = package_requirements[6]
	max_ir = package_requirements[7]

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
		arduino_x, arduino_y = arduino_pos
		translated_path = translate_path(arduino_x, arduino_y)
		print(translated_path)
		ev3_ser.write(translated_path.encode())
		try:
			while (True):
				# reSend = input("send again? y/n")
				rec = ev3_ser.readline().decode().strip()
				try:
					x = int(rec[0]) - .5
					y = int(rec[1]) - .5
				except ValueError:
					x = 2
					y = 2
					print("Undecodable message: {}".format(rec))
				if x > 0 and x < 3 and y > 0 and y < 3:
					stream.write({'x': x, 'y': y})
				else:
					print('Invalid data! {}'.format(rec))
		except KeyboardInterrupt:
			pass
	else:
		print("Requirements not fulfilled.")
		print("Moving package to another destination.")
		translated_path = translate_path(alt_pos)
		print(translated_path)
		ev3_ser.write(translated_path)
		try:
			while (True):
				# reSend = input("send again? y/n")
				rec = ev3_ser.readline().decode().strip()
				x = int(rec[0])
				y = rec(rec[1])
				if x > 0 and x < 3 and y > 0 and y < 3:
					stream.write({'x': x, 'y': y})
				else:
					print('Invalid data!')
				print(rec)
		except KeyboardInterrupt:
			pass


#reload(sys)
#sys.setdefaultencoding('utf8')
run_menu()
