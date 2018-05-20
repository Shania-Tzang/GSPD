#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time

class EV3Robot:
	__linePassed = 0			# no of line passed = no of grid passed

	# Init robot with sensors below, can change the port as needed
	def __init__(self):
		self.__leftWheel = ev3.LargeMotor('outB')
		self.__rightWheel = ev3.LargeMotor('outD')
		self.__gyro = ev3.GyroSensor('in2')			# measure the difference in angle when turning
		self.__color = ev3.ColorSensor('in1')		
		self.__liftArm = ev3.MediumMotor('outC')     # init lift arm (medium motor)
		self.__color.mode = 'COL-COLOR'				# put color sensor in COL-COLOR mode that can only detect 7 types of color
		self.__gyro.mode = 'GYRO-ANG'

	# Go straight for some milliseconds or forever. Speed is suggested to be 500rpm
	def goStraight(self, speed = 100, millisecond = 0):
		if millisecond != 0:
			self.__leftWheel.run_timed(time_sp=millisecond, speed_sp=speed)
			self.__rightWheel.run_timed(time_sp=millisecond, speed_sp=speed)
			time.sleep(millisecond/1000)
		else:	
			self.__leftWheel.run_forever(speed_sp=speed)
			self.__rightWheel.run_forever(speed_sp=speed)

	# Spin around at its standpoint to the left
	def rotateLeft(self, speed = 100, millisecond = 0):
		if millisecond != 0:
			self.__leftWheel.run_timed(time_sp = millisecond, speed_sp = -speed)
			self.__rightWheel.run_timed(time_sp = millisecond, speed_sp = speed)
			time.sleep(millisecond/1000)
		else:	
			self.__leftWheel.run_forever(speed_sp=-speed)
			self.__rightWheel.run_forever(speed_sp=speed)
		while True:
			print(self.getRotateAngle())
			if (self.getRotateAngle() <= -88):  # This angle can be adjusted bas$
				self.stop()
				break
			time.sleep(0.01)

	# Spin around at its standpoint to the right
	def rotateRight(self, speed = 100, millisecond = 0):
		self.resetGyro()
		if millisecond != 0:
			self.__leftWheel.run_timed(time_sp = millisecond, speed_sp = speed)
			self.__rightWheel.run_timed(time_sp = millisecond, speed_sp = -speed)
			time.sleep(millisecond/1000)
		else:	
			self.__leftWheel.run_forever(speed_sp=speed)
			self.__rightWheel.run_forever(speed_sp=-speed)
			while True:
				print(self.getRotateAngle())
				if(self.getRotateAngle() >= 88):       # This angle can be adjusted bas$
					self.stop()
					break
				time.sleep(0.01)
	
	# Drift left until reaching 90 degree. Experiments show that drifting have the most accuracy for gyrosensor	
	def turnLeft(self, speed = 500, millisecond = 0):
		self.resetGyroGyro()
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

	def resetPassedLine(self):
		self.__linePassed = 0

	def getColor(self):
		return self.__color.color

	def getLinePassed(self):
		return self.__linePassed

	def setLinePassed(self, no):
		self.__linePassed = no

	def liftForkArm(self, speed = 80):
		self.__liftArm.run_timed(time_sp=1000, speed_sp=speed)
	
	def lowerForkArm(self, speed = -80):
		self.__liftArm.run_timed(time_sp=1000, speed_sp=speed)
