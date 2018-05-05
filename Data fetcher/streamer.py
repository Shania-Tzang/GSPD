# Import PySerial library
import serial

# Establish serial connection to the Arduino
channel = serial.Serial('/dev/tty.team1ARDUINO-DevB')

# Based on: https://plot.ly/raspberry-pi/tmp36-temperature-tutorial/
import plotly.plotly as py # plotly library
import json # used to parse config.json
import datetime # log and plot current time

# Parse the configuration
with open('./config.json') as config_file:
    plotly_user_config = json.load(config_file)

# Sign in to plotly
py.sign_in(
    plotly_user_config["plotly_username"],
    plotly_user_config["plotly_api_key"]
)

# Here we get the 4 stream IDs
stream_id1 = plotly_user_config['plotly_streaming_tokens'][0]
stream_id2 = plotly_user_config['plotly_streaming_tokens'][1]
stream_id3 = plotly_user_config['plotly_streaming_tokens'][2]
stream_id4 = plotly_user_config['plotly_streaming_tokens'][3]

# Create a plot
url1 = py.plot([
        {
            'x': [],
            'y': [],
            'type': 'scatter',
            'name': 'Humidity (%)',
            'stream': {
                'token': stream_id1, 'maxpoints': 200
            }
        },
        {
            'x': [],
            'y': [],
            'type': 'scatter',
            'name': 'Temperature (°C)',
            'stream': {
                'token': stream_id2, 'maxpoints': 200
            }
        }
    ],
    filename='Arduino Sensors data - Area conditions',
    fileopt='overwrite',
    auto_open=False)

url2 = py.plot([
        {
            'x': [],
            'y': [],
            'type': 'scatter',
            'name': 'VIS',
            'stream': {
                'token': stream_id3, 'maxpoints': 200
            }
        },
        {
            'x': [],
            'y': [],
            'type': 'scatter',
            'name': 'IR',
            'stream': {
                'token': stream_id4, 'maxpoints': 200
            }
        }
    ],
    filename='Arduino Sensors data - Light conditions',
    fileopt='overwrite',
    auto_open=False)

print("View your first streaming graph here: {}".format(url1))
print("View your second streaming graph here: {}".format(url2))

stream1 = py.Stream(stream_id1)
stream1.open()
stream2 = py.Stream(stream_id2)
stream2.open()
stream3 = py.Stream(stream_id3)
stream3.open()
stream4 = py.Stream(stream_id4)
stream4.open()

# Fetch the data
while True:
    #print(ser.readline())
    # Read one line, decode it from bytes and strip spaces at left and right
    data = channel.readline().decode().strip()
    
    # Check everything works
    print(data)

    # Split the data, given the separator
    data = data.split('|')
    # Read the data properly
    reworked_data = []
    for sensor in data:
        description, value = sensor.split(':')
        value = float(value)
        reworked_data.append((description, value))
    #print(reworked_data)

    # write the data to plotly
    stream1.write(
        {
            'x': datetime.datetime.now(),
            'y': reworked_data[0][1]
        })
    stream2.write(
        {
            'x': datetime.datetime.now(),
            'y': reworked_data[1][1]
        })
    stream3.write(
        {
            'x': datetime.datetime.now(),
            'y': reworked_data[2][1]
        })
    stream4.write(
        {
            'x': datetime.datetime.now(),
            'y': reworked_data[3][1]
        })
