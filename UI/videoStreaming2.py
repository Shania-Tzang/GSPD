#!/usr/bin/env python
from flask import Flask, render_template, Response, url_for
import cv2
from time import sleep

app = Flask(__name__)
vc = cv2.VideoCapture(0)

@app.route('/')
def index():
    """Video streaming home page."""
    #return render_template('index.html')
    return 'Are you maybe interested in <a href="{}">this</a>?'.format(url_for('video_feed'))


def gen():
    """Video streaming generator function."""
    while True:
        rval, frame = vc.read()
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
        sleep(0.1)


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='localhost', debug=True, threaded=True)
