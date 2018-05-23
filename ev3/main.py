import sys
import time
import robot

# Robot get destination, go to it, then lower the cargo, move back a bit, then return to starting position
if __name__ == "__main__":
	r = robot.EV3Robot()
	try:
		r.setBeginPos([1,1])
		r.setDesPos([4,3])
		r.setOrientation([1,0])
		r.deliver()
	except KeyboardInterrupt:
		#print(e)
		r.stop()