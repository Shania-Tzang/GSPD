# Import PySerial library
import serial

# Based on: https://plot.ly/raspberry-pi/tmp36-temperature-tutorial/
# Plotly library
import plotly.plotly as py
import plotly.graph_objs as go
import json # used to parse config.json
import datetime # log and plot current time
import time

from os.path import abspath, dirname, join

channel = serial.Serial('/dev/tty.team1ARDUINO-DevB')

class Streamer:

    def __init__(self):
        self.is_waiting = False
        self.stream_is_busy = False

    def run(self):
        # Establish serial connection to the Arduino
        channel.close()
        channel.open()

        json_path = join(dirname(abspath(__file__)), 'config.json')

        # Parse the configuration
        with open(json_path) as config_file:
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

        # Create the proper stream objects
        stream_config_1 = go.Stream(token=stream_id1, maxpoints=200)
        stream_config_2 = go.Stream(token=stream_id2, maxpoints=200)
        stream_config_3 = go.Stream(token=stream_id3, maxpoints=200)
        stream_config_4 = go.Stream(token=stream_id4, maxpoints=200)

        plot1 = go.Scatter(x = [], y = [], stream=stream_config_1, name='Humidity (%)')
        plot2 = go.Scatter(x = [], y = [], stream=stream_config_2, name='Temperature (C)')
        plot3 = go.Scatter(x = [], y = [], stream=stream_config_3, name='VIS')
        plot4 = go.Scatter(x = [], y = [], stream=stream_config_4, name='IR')

        # Create a plot
        url1 = py.plot([plot1, plot2],
                       filename='Arduino Sensors data - Area conditions',
                       fileopt='overwrite',
                       auto_open=False)

        url2 = py.plot([plot3, plot4],
                       filename='Arduino Sensors data - Light conditions',
                       fileopt='overwrite',
                       auto_open=False)

        #print("View your first streaming graph here: {}".format(url1))
        #print("View your second streaming graph here: {}".format(url2))

        stream1 = py.Stream(stream_id1)
        stream1.open()
        stream2 = py.Stream(stream_id2)
        stream2.open()
        stream3 = py.Stream(stream_id3)
        stream3.open()
        stream4 = py.Stream(stream_id4)
        stream4.open()

        # Fetch the data
        try:
            while True:
                if (self.stream_is_busy == False):
                    #print(ser.readline())
                    # Read one line, decode it from bytes and strip spaces at left and right

                    self.is_waiting = False

                    data = channel.readline().decode().strip()

                    # Check everything works
                    #print(data, end='\r')

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
            
                    self.is_waiting = True
                    time.sleep(5)
                    
        except KeyboardInterrupt:
            print('\nClosing')
