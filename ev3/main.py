import sys
import time
import robot

# Robot get destination, go to it, then lower the cargo and move back a bit
if __name__ == "__main__":
	r = robot.EV3Robot()
	try:
		r.setDesPos([4,3])
		r.go()
		r.goStraight(-500, 700)
	except KeyboardInterrupt:
		#print(e)
		r.stop()