import sys
import time
import robot

def passedBlackLine(robot, state):
	col = robot.getColor()
	if col == 1 and state == 0:
		state = 1
	elif col != 1 and state == 1:
		robot.setLinePassed(robot.getLinePassed() + 1)
		state = 0
	return state

# Robot will run straight until it has met 2 black lines, then turn right and stop.
if __name__ == "__main__":
	r = robot.EV3Robot()
	try:
		r.goStraight()
		state = 0
		while True:
			state = passedBlackLine(r, state)
			if r.getLinePassed() == 2:
				r.stop()
				r.turnRight()
				break
			time.sleep(0.01)
	except KeyboardInterrupt:
		#print(e)
		r.stop()