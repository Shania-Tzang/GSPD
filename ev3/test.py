#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time
import sys

def go_straight(left, right, millisecond=0):
	if millisecond != 0:
		left.run_timed(time_sp=millisecond, speed_sp=-500)
		right.run_timed(time_sp=millisecond, speed_sp=-500)
		time.sleep(millisecond/1000)
	else:	
		left.run_forever(speed_sp=-500)
		right.run_forever(speed_sp=-500)

def rotate_left(left, right, millisecond=0):
	if millisecond != 0:
		left.run_timed(time_sp = millisecond, speed_sp = 1000)	
		right.run_timed(time_sp = millisecond, speed_sp = -1000)
		time.sleep(millisecond/1000)
	else:	
		left.run_forever(speed_sp=1000)
		right.run_forever(speed_sp=-1000)

def rotate_right(left, right, millisecond=0):
	if millisecond != 0:
		left.run_timed(time_sp = millisecond, speed_sp = -1000)	
		right.run_timed(time_sp = millisecond, speed_sp = 1000)
		time.sleep(millisecond/1000)
	else:	
		left.run_forever(speed_sp=-1000)
		right.run_forever(speed_sp=1000)
	
def turn_left(left, right, gyro, millisecond=0):
	reset(gyro)
	if millisecond != 0:
		right.run_timed(time_sp = millisecond, speed_sp = -1000)
		left.run_timed(time_sp = millisecond, speed_sp = -500)
		time.sleep(millisecond/1000)
	else:
		right.run_forever(speed_sp = -1000)
		left.run_forever(speed_sp = -500)
		while True:
			if(getRotateAngle(gyro) <= -88):
				stop(left, right)
				break
			time.sleep(0.01)

def turn_right(left, right, gyro, millisecond=0):
	reset(gyro)
	if millisecond != 0:
		left.run_timed(time_sp = millisecond, speed_sp = -1000)
		right.run_timed(time_sp = millisecond, speed_sp = -500)
		time.sleep(millisecond/1000)
	else:		
		left.run_forever(speed_sp=-1000)
		right.run_forever(speed_sp=-500)
		while True:
			if(getRotateAngle(gyro) >= 88):
				stop(left, right)
				break
			time.sleep(0.01)

def stop(left, right):
	left.stop()
	right.stop()

def getRotateAngle(gyro):
	g = gyro.angle
	return g

def reset(gyro):
	gyro.mode = 'GYRO-RATE'
	gyro.mode = 'GYRO-ANG'
	
# def countLine(color):
# 	flag = 0
# 	while True:
# 		col = color.color
# 		if col == 1 and flag == 0:
# 			flag = 1
# 		elif col == 1 and flag == 1:
# 			return 1
# 		time.sleep(0.01)

if __name__ == "__main__":
	m = ev3.LargeMotor('outB')
	n = ev3.LargeMotor('outD')
	gyro = ev3.GyroSensor('in2')
	gyro.mode = 'GYRO-ANG'
	color = ev3.ColorSensor('in1')
	color.mode = 'COL-COLOR'
	# while True:
	# 	print(color.color)
	# sys.exit(1)
	count = 0
	flag = 0
	go_straight(m, n)
	time1 = time.time()
	while True:
		col = color.color
		if col == 1 and flag == 0:
			flag = 1
		elif col != 1 and flag == 1:
			flag = 2
		elif col != 1 and flag == 2:
			count += 1
			print(count)
			if count == 2:
				stop(m,n)
				turn_right(m, n, gyro)
				break
			flag = 0
		print(str(col) + " " + str(flag))
		time.sleep(0.01)
		# print(color.color)
		# time.sleep(0.01)
		# if time.time() - time1 >= 5.0:
		# 	stop(m, n)
		# 	break
	

	# turn_left(m, n, gyro)
	# print(str(getRotateAngle(gyro)) + " " + gyro.units)
	# reset(gyro)
	# go_straight(m, n, 2000)
	# rotate_right(m, n, 2000)
	# print(str(getRotateAngle(gyro)) + " " + gyro.units)
	# time.sleep(0.5)
	# reset(gyro)

	#rotate_right(m, n, 1000)
	# turn_right(m, n, gyro, 500)
	# print(getRotateAngle(gyro))
	# time.sleep(1)
	# rotate_right(m, n, 1000)
	# print(getRotateAngle(gyro))

	# go_straight(m,n)
	# time1 = time.time()	
	# q = ev3.UltrasonicSensor('in4')
	# while True:
	# 	print(q.distance_centimeters)
	# 	if q.distance_centimeters <= 30.0:
	# 		stop(m,n)
	# 		rotate(m,n)			
	# 	else:
	# 		go_straight(m,n)
	# 	time.sleep(0.1)
	# 	if time.time() - time1 > 60.0:
	# 		stop(m,n)
	# 		sys.exit(1)
	# 