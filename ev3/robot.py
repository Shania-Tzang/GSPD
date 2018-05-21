#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time
import random

class EV3Robot:
	__linePassed = 0			# no of line passed = no of grid passed
	__currentPos = [1,1]
	__desPos = []

	# Init robot with sensors below, can change the port as needed
	def __init__(self):
		self.__leftWheel = ev3.LargeMotor('outB')
		self.__rightWheel = ev3.LargeMotor('outD')
		self.__arm = ev3.MediumMotor('outC')
		self.__gyro = ev3.GyroSensor()			# measure the difference in angle when turning
		self.__color = ev3.ColorSensor()		
		self.__color.mode = 'COL-COLOR'					# put color sensor in COL-COLOR mode that can only detect 7 types of color
		self.__gyro.mode = 'GYRO-ANG'

	# Go straight for some milliseconds or forever. Speed is suggested to be 500rpm
	def goStraight(self, speed = 500, millisecond = 0):
		if millisecond != 0:
			self.__leftWheel.run_timed(time_sp=millisecond, speed_sp=-speed)
			self.__rightWheel.run_timed(time_sp=millisecond, speed_sp=-speed)
			time.sleep(millisecond/1000)
		else:	
			self.__leftWheel.run_forever(speed_sp=-speed)
			self.__rightWheel.run_forever(speed_sp=-speed)

	# Spin around at its standpoint to the left, timed or forever
	def rotateLeft(self, speed = 500, millisecond = 0):
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
				if(self.getRotateAngle() <= -85):	# This angle can be adjusted based on experiment
					self.stop()
					break
				time.sleep(0.01)

	# Spin around at its standpoint to the right, timed or forever
	def rotateRight(self, speed = 500, millisecond = 0):
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
				if(self.getRotateAngle() >= 85):	# This angle can be adjusted based on experiment
					self.stop()
					break
				time.sleep(0.01)
		
	# Drift left until reaching 90 degree. Experiments show that drifting have the most accuracy for gyrosensor	
	def turnLeft(self, speed = 500, millisecond = 0):
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
	def turnRight(self, speed = 500, millisecond = 0):
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
	def raiseArm(self, time = 500, speed = 100):
		self.__arm.run_timed(time_sp = time, speed_sp = speed)
		time.sleep(time/1000)

	def lowerArm(self, millisecond = 600, speed = 100):
		self.__arm.run_timed(time_sp = millisecond, speed_sp = -speed)
		time.sleep(millisecond/1000)

	# Set destination
	def setDesPos(self, des):
		self.__desPos = des

	# Check if robot has passed a black line == passed a grid
	def passedBlackLine(self, state):
		col = self.getColor()
		if col == 1 and state == 0:
			state = 1
		elif col != 1 and state == 1:
			self.setLinePassed(self.getLinePassed() + 1)
			state = 0
		return state	

	# Way calculation and moving function
	def calculateDaWay(self):
		if self.__desPos[1] - self.__currentPos[1]:
			# 2 strategies to go, choosen randomly
			way1 = {"1":"straight-" + str(self.__desPos[0] - self.__currentPos[0]),"2":"right-" + str(self.__desPos[1] - self.__currentPos[1])}
			way2 = {"2":"straight-" + str(self.__desPos[0] - self.__currentPos[0]),"1":"right-" + str(self.__desPos[1] - self.__currentPos[1])}
		return [way1, way2]
			
	def go(self):
		if random.randint(1,2) == 1:		# Choose strategy
			way = self.calculateDaWay()[0]
		else:
			way = self.calculateDaWay()[1]
		state = 0
		parseway1 = way["1"].split('-')
		parseway2 = way["2"].split('-')
		# First half of the way, go straight
		if parseway1[0] == "straight":		# Straight first
			if int(parseway1[1]) != 0:		# Check if destination is at the same row
				self.goStraight()
				while True:					# Count grid until reaching first position
					state = self.passedBlackLine(state)
					if self.getLinePassed() == int(parseway1[1]):
						if int(parseway2[1] != 0): # If destination is not reached => move up a bit
							time.sleep(0.7)
						self.stop()
						state = 0
						self.setLinePassed(0)
						break
					time.sleep(0.01)
			# Second half of the way, go left or right
			if parseway2[0] == "right" and int(parseway2[1]) != 0: # Check if destination is at the same column
				self.rotateRight()
			elif parseway2[0] == "left" and int(parseway2[1]) != 0:
				self.rotateLeft()
			else:
				self.lowerArm()	# If same column => at destination => drop cargo
				return
			self.goStraight()
			while True:
				state = self.passedBlackLine(state)
				if self.getLinePassed() == int(parseway2[1]):
					self.stop()
					self.lowerArm()
					state = 0
					self.setLinePassed(0)
					break
				time.sleep(0.01)
		# First half of the way, go left
		elif parseway1[0] == "left":
			if int(parseway1[1]) != 0:
				self.rotateLeft()
				self.goStraight()
				while True:
					state = self.passedBlackLine(state)
					if self.getLinePassed() == int(parseway1[1]):
						if int(parseway2[1] != 0): # If destination is not reached => move up a bit
							time.sleep(0.7)
						self.stop()
						state = 0
						self.setLinePassed(0)
						break
					time.sleep(0.01)
			if int(parseway2[1]) == 0:
				self.lowerArm()
				return
			self.rotateRight()
			self.goStraight()
			while True:
				state = self.passedBlackLine(state)
				if self.getLinePassed() == int(parseway2[1]):
					self.stop()
					self.lowerArm()
					state = 0
					self.setLinePassed(0)
					break
				time.sleep(0.01)
		# First half of the way, go right
		else:
			if int(parseway1[1]) != 0:
				self.rotateRight()
				self.goStraight()
				while True:
					state = self.passedBlackLine(state)
					if self.getLinePassed() == int(parseway1[1]):
						if int(parseway2[1] != 0): # If destination is not reached => move up a bit
							time.sleep(0.7)
						self.stop()
						state = 0
						self.setLinePassed(0)
						break
					time.sleep(0.01)
			if int(parseway2[1]) == 0:
				self.lowerArm()
				return
			self.rotateLeft()
			self.goStraight()
			while True:
				state = self.passedBlackLine(state)
				if self.getLinePassed() == int(parseway2[1]):
					self.stop()
					self.lowerArm()
					state = 0
					self.setLinePassed(0)
					break
				time.sleep(0.01)
