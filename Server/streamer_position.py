from random import randint

# Based on: https://plot.ly/raspberry-pi/tmp36-temperature-tutorial/
# Plotly library
import plotly.plotly as py
import plotly.graph_objs as go
import json  # used to parse config.json
import datetime  # log and plot current time

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

try:
    while True:
        # Request input manually
        #x = input('X (between 1 and 3): ')
        #y = input('Y (between 1 and 3): ')
        ## Convert the data
        #x = int(x) - .5
        #y = int(y) - .5
        # Random showoff!
        x = randint(1, 3) - .5
        y = randint(1, 3) - .5
        if x > 0 and x < 3 and y > 0 and y < 3:
            stream.write({'x': x, 'y': y})
        else:
            print('Invalid data!')
except KeyboardInterrupt:
    pass
