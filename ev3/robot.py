#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time
import random

class EV3Robot():
	__linePassed = 0			# no of line passed = no of grid passed
	__currentPos = []
	__desPos = []
	__orientation = []			# [1,0]: North, [0,1]: East, [-1,0]: South, [0,-1]: West
	__beginPos = []
	__path = [(1,1)]
	__pathCursor = 0

	# Init robot with sensors below, can change the port as needed
	def __init__(self, socket):
		self.__leftWheel = ev3.LargeMotor('outB')
		self.__rightWheel = ev3.LargeMotor('outD')
		self.__arm = ev3.MediumMotor('outC')
		self.__gyro = ev3.GyroSensor()			# measure the difference in angle when turning
		self.__color = ev3.ColorSensor()		
		self.__color.mode = 'COL-COLOR'					# put color sensor in COL-COLOR mode that can only detect 7 types of color
		self.__gyro.mode = 'GYRO-ANG'
		self.__socket = socket

	# Go straight for some milliseconds or forever. Speed is suggested to be 500rpm
	def goStraight(self, speed = 200, millisecond = 0):
		if millisecond != 0:
			self.__leftWheel.run_timed(time_sp=millisecond, speed_sp=speed)
			self.__rightWheel.run_timed(time_sp=millisecond, speed_sp=speed)
			time.sleep(millisecond/1000)
		else:	
			self.__leftWheel.run_forever(speed_sp=speed)
			self.__rightWheel.run_forever(speed_sp=speed)

	# Spin around at its standpoint to the left, timed or forever
	def rotateLeft(self, speed = 200, millisecond = 0):
		#self.transmit(self.__socket, "L")
		self.resetGyro()
		if millisecond != 0:
			#self.resetGyro()
			self.__leftWheel.run_timed(time_sp = millisecond, speed_sp = -speed)	
			self.__rightWheel.run_timed(time_sp = millisecond, speed_sp = speed)
			#print(self.getRotateAngle())
			time.sleep(millisecond/1000)
		else:	
			self.__leftWheel.run_forever(speed_sp=-speed)
			self.__rightWheel.run_forever(speed_sp=speed)
			while True:
				print(self.getRotateAngle())
				if(abs(self.getRotateAngle()) >= 84):	# This angle can be adjusted based on experiment
					self.stop()
					break
				time.sleep(0.01)
		#self.resetGyro()

	# Spin around at its standpoint to the right, timed or forever
	def rotateRight(self, speed = 200, millisecond = 0):
		#self.transmit(self.__socket, "R")
		self.resetGyro()
		if millisecond != 0:
			#self.resetGyro()
			self.__leftWheel.run_timed(time_sp = millisecond, speed_sp = speed)	
			self.__rightWheel.run_timed(time_sp = millisecond, speed_sp = -speed)
			#print(self.getRotateAngle())
			time.sleep(millisecond/1000)
		else:	
			self.__leftWheel.run_forever(speed_sp=speed)
			self.__rightWheel.run_forever(speed_sp=-speed)
			while True:
				print(self.getRotateAngle())
				if(self.getRotateAngle() >= 84):	# This angle can be adjusted based on experiment
					self.stop()
					break
				time.sleep(0.01)
		#self.resetGyro()

	def rotate180(self, speed = 200, millisecond = 0, angle = 165):
		#self.transmit(self.__socket, "180")
		self.resetGyro()
		if millisecond != 0:
			#self.resetGyro()
			self.__leftWheel.run_timed(time_sp = millisecond, speed_sp = -speed)	
			self.__rightWheel.run_timed(time_sp = millisecond, speed_sp = speed)
			#print(self.getRotateAngle())
			time.sleep(millisecond/1000)
		else:	
			self.__leftWheel.run_forever(speed_sp=-speed)
			self.__rightWheel.run_forever(speed_sp=speed)
			while True:
				if(abs(self.getRotateAngle()) >= angle):	# This angle can be adjusted based on experiment
					self.stop()
					break
				time.sleep(0.01)
		self.resetGyro()
		
	# Drift left until reaching 90 degree. Experiments show that drifting have the most accuracy for gyrosensor	
	def turnLeft(self, speed = 200, millisecond = 0):
		self.resetGyro()
		if millisecond != 0:
			self.__rightWheel.run_timed(time_sp = millisecond, speed_sp = -speed)
			self.__leftWheel.run_timed(time_sp = millisecond, speed_sp = -speed)
			time.sleep(millisecond/1000)
		else:
			self.__rightWheel.run_forever(speed_sp = -speed)
			self.__leftWheel.run_forever(speed_sp = -speed/2)
			while True:
				if(self.getRotateAngle() <= -88):	# This angle can be adjusted based on experiment
					self.stop()
					break
				time.sleep(0.01)

	# Drift right until reaching 90 degree
	def turnRight(self, speed = 200, millisecond = 0):
		self.resetGyro()
		if millisecond != 0:
			self.__leftWheel.run_timed(time_sp = millisecond, speed_sp = -speed)
			self.__rightWheel.run_timed(time_sp = millisecond, speed_sp = -speed/2)
			time.sleep(millisecond/1000)
		else:		
			self.__leftWheel.run_forever(speed_sp=-speed)
			self.__rightWheel.run_forever(speed_sp=-speed/2)
			while True:
				if(self.getRotateAngle() >= 88):	# This angle can be adjusted based on experiment
					self.stop()
					break
				time.sleep(0.01)

	# Stop both wheel from running forever
	def stop(self):
		self.__leftWheel.stop()
		self.__rightWheel.stop()

	# Get the difference in angle provided by GyroSensor
	def getRotateAngle(self):
		return self.__gyro.angle

	# Reset the angle to 0	
	def resetGyro(self):
		self.__gyro.mode = 'GYRO-RATE'
		self.__gyro.mode = 'GYRO-ANG'

	# Get color sensor's color
	def getColor(self):
		return self.__color.color

	# linePassed getter-setter
	def getLinePassed(self):
		return self.__linePassed

	def setLinePassed(self, no):
		self.__linePassed = no

	# Arm function
	def raiseArm(self, millisecond = 600, speed = 100):
		self.__arm.run_timed(time_sp = millisecond, speed_sp = speed)
		time.sleep(millisecond/1000)

	def lowerArm(self, millisecond = 600, speed = 100):
		self.__arm.run_timed(time_sp = millisecond, speed_sp = -speed)
		time.sleep(millisecond/1000)

	def setBeginPos(self, begin):
		self.__beginPos = begin
		self.setCurPos(begin)

	# Set current position
	def setCurPos(self, cur):
		self.__currentPos = cur

	# Set destination
	def setDesPos(self, des):
		self.__desPos = des

	# Set orientation
	def setOrientation(self, orientation):
		self.__orientation = orientation

	# Check if robot has passed a black line == passed a grid
	def passedBlackLine(self, state):
		col = self.getColor()
		if col == 1 and state == 0:
			state = 1
		elif col != 1 and state == 1:
			self.setLinePassed(self.getLinePassed() + 1)
			state = 0
		return state	

	## New way to calculate road and move

	## Set a mid-destination point. Ex: currentPos: 1,1; desPos: 3,4 => temPos: 1,4 or 3,1
	def setTempDesPoint(self):
		point1 = [self.__desPos[0], self.__currentPos[1]]
		point2 = [self.__currentPos[0], self.__desPos[1]]
		if random.randint(1,2) == 1:
			return point1
		else:
			return point2

	## Solve the problem: Robot and tempDes on the same line (row or column), robot is oriented randomly, how can robot move to tempDes
	def goSameLine(self, tempDes, finalDes = False):
		if self.__currentPos[0] == tempDes[0] and self.__currentPos[1] == tempDes[1]: # If currentDes == tempDes
			if finalDes == True:													  # Already finalDes => release cargo	
				self.lowerArm()
				self.goStraight(-200,500)
				self.raiseArm()
				return
			else:
				return
		newOrientation = [tempDes[0] - self.__currentPos[0], tempDes[1] - self.__currentPos[1]]	# direction vector from robot to tempDes
		if self.__orientation[0] * newOrientation[0] + self.__orientation[1] * newOrientation[1] != 0:
			if self.__orientation[0] * newOrientation[0] > 0 or self.__orientation[1] * newOrientation[1] > 0:	# current orientation and direction vector have same direction
				pass
			else:	
				self.rotate180()	# current orientation and direction vector have opposite direction
				#self.goStraight(-200,800)
		elif self.__orientation[0] * newOrientation[1] - self.__orientation[1] * newOrientation[0] > 0: # current orientation is to the left of direction vector
			self.rotateRight()
			#self.goStraight(-200,500)
		else:	# current orientation is to the right of direction vector
			self.rotateLeft()
			#self.goStraight(-200,800)
		self.__orientation = newOrientation	# update new orientation
		state = 0
		xory = 0	# hold temp value whether x value or y value of newOrientation is different from 0
		if newOrientation[0] != 0:			# calculate number of lines to pass
			lines = abs(newOrientation[0])
			xory = 0
		else:
			lines = abs(newOrientation[1])
			xory = 1

		self.goStraight()
		currentPassed = 0 # begin moving
		while True:
			print("path " + str(self.__path))
			state = self.passedBlackLine(state)
			if currentPassed != str(self.getLinePassed()) and self.__pathCursor < len(self.__path):
				print ("debug lines passed" + str(self.getLinePassed()))
				self.transmit(self.__socket, str(self.__path[self.__pathCursor][1]) + str(self.__path[self.__pathCursor][0]))
				print (self.__path[self.__pathCursor])
				self.incrementPathCursor()
			currentPassed = str(self.getLinePassed())
			if self.getLinePassed() == lines:
				self.stop()
				self.setLinePassed(0)
				if finalDes == True:		# if reaching destination then release cargo
					self.lowerArm()
					self.goStraight(-200,500)
					self.raiseArm()
				else:
					self.goStraight(200,1200) # else move up a bit for robot to be at the center of the grid
				break
			time.sleep(0.01)
		# update current position
		if finalDes == False:
			self.__currentPos = tempDes
		else:
			if newOrientation[xory] > 0:
				self.__currentPos[xory] = self.__currentPos[xory] + newOrientation[xory] - 1
			else:
				self.__currentPos[xory] = self.__currentPos[xory] + newOrientation[xory] + 1

	def deliver(self):
		midPoint =self.setTempDesPoint()
		self.__path = calc_path([],[1,1],midPoint,self.__desPos)
		self.goSameLine(midPoint, False)
		self.goSameLine(self.__desPos, True)
		# Go back home
		prevDes = self.__desPos
		self.__desPos = self.__beginPos
		tempNewBeginPos = self.__path[self.__pathCursor-2]
		print(str(tempNewBeginPos))
		midPoint2 = self.setTempDesPoint()
		print("midpint: " +  str(midPoint2))
		print("DEBUG " + str(self.__path[self.__pathCursor - 2]))
		self.__path = calc_path_back([], self.__path[self.__pathCursor-2], midPoint2, self.__beginPos)
		print(str(self.__path))
		self.resetPathCursor()
		self.goSameLine(midPoint2, False)
		self.goSameLine(self.__desPos, False)
		print("delivered")

	def transmit(self, bltsocket, msg):
		bltsocket.send(msg + "\n")

	def resetPathCursor(self):
		self.__pathCursor = 0

	def incrementPathCursor(self):
		self.__pathCursor = self.__pathCursor + 1

def calc_path(path, startpoint, midpoint, destpoint):
	print("stuck")
	if (midpoint[0] == startpoint[0]):             # mY == sY => increment X
		path.append([startpoint[0], startpoint[1]])
		newpoint = [startpoint[0], startpoint[1]]
		newpoint[1] += 1

		while (newpoint[1] < midpoint[1]):
			path.append([newpoint[0], newpoint[1]])
			newpoint[1] += 1
		path.append([midpoint[0], midpoint[1]])
		newpoint2 = [midpoint[0], midpoint[1]]
		newpoint2[0] += 1

		while (newpoint2[0] < destpoint[0]):
			path.append([newpoint2[0], newpoint2[1]])
			newpoint2[0] += 1
		path.append(destpoint)

	else:                            # mY != sY => increment Y
		path.append([startpoint[0], startpoint[1]])
		newpoint = [startpoint[0], startpoint[1]]
		newpoint[0] += 1

		while (newpoint[0] < midpoint[0]):
			path.append([newpoint[0], newpoint[1]])
			newpoint[0] += 1
		path.append([midpoint[0], midpoint[1]])
		newpoint2 = [midpoint[0], midpoint[1]]
		newpoint2[1] += 1

		while (newpoint2[1] < destpoint[1]):
			path.append([newpoint2[0], newpoint2[1]])
			newpoint2[1] += 1
		path.append([destpoint[0], destpoint[1]])

	return path

def calc_path_back(path, startpoint, midpoint, destpoint):
	print ("in")
	if (midpoint[0] == startpoint[0]):             # mY == sY => increment X
		path.append([startpoint[0], startpoint[1]])
		newpoint = [startpoint[0], startpoint[1]]
		newpoint[1] -= 1

		while (newpoint[1] > midpoint[1]):
			path.append([newpoint[0], newpoint[1]])
			newpoint[1] -= 1
		path.append([midpoint[0], midpoint[1]])
		newpoint2 = [midpoint[0], midpoint[1]]
		newpoint2[0] -= 1

		while (newpoint2[0] > destpoint[0]):
			path.append([newpoint2[0], newpoint2[1]])
			newpoint2[0] -= 1
			print ("stuck")
		path.append(destpoint)
		print ("123")

	else:                            # mY != sY => increment Y
		path.append([startpoint[0], startpoint[1]])
		newpoint = [startpoint[0], startpoint[1]]
		newpoint[0] -= 1

		while (newpoint[0] > midpoint[0]):
			path.append([newpoint[0], newpoint[1]])
			newpoint[0] -= 1
		path.append([midpoint[0], midpoint[1]])
		newpoint2 = [midpoint[0], midpoint[1]]
		newpoint2[1] -= 1

		while (newpoint2[1] > destpoint[1]):
			path.append([newpoint2[0], newpoint2[1]])
			newpoint2[1] -= 1
		path.append([destpoint[0], destpoint[1]])

	print ("done")
	return path
