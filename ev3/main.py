import sys
import robot

def passedBlackLine(robot):
		col = robot.__color.color
		if col == 1 and robot.__state == 0:
			robot.__state = 1
		elif col != 1 and robot.__state == 1:
			robot.__linePassed += 1
			robot.__state = 0

# Robot will run straight until it has met 2 black lines, then turn right and stop.
if __name__ == "__main__":
	robot = robot.EV3Robot()
	robot.goStraight()
	while True:
		passedBlackLine(robot)
		if robot.__linePassed == 2:
			robot.stop()
			robot.turnRight()
			break