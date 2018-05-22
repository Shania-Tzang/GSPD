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

		## Main for new move and way calculation function (NOT YET TESTED)
		# r.setBeginPos([2,1])
		# r.setDesPos([4,3])
		# r.setOrientation([1,0])
		# r.deliver()
	except KeyboardInterrupt:
		#print(e)
		r.stop()