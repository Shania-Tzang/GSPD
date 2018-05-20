from bluetooth import *
import sys
import time
import robot_uppsala


server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
				   service_id = uuid,
				   service_classes = [ uuid, SERIAL_PORT_CLASS ],
				   profiles = [ SERIAL_PORT_PROFILE ],
#                   protocols = [ OBEX_UUID ]
					)

#GLOBAL DEBUG VARS
LINES_TO_PASS = 2
SECOND_LINES_TO_PASS = 2

def passedBlackLine(robot, state):
	col = robot.getColor()
	print ("COLOR " + str(col))
	if col == 1 and state == 0:
		state = 1
	elif col != 1 and state == 1:
		robot.setLinePassed(robot.getLinePassed() + 1)
		state = 0
	return state


def run(numOfLines, rotation):
	r.goStraight()
	state = 0
	while True:
		state = passedBlackLine(r, state)
		print ("LINES PASSED " + str(r.getLinePassed()))
		if r.getLinePassed() == numOfLines:
			r.stop()
			if rotation == "right":
				r.rotateRight()
			elif rotation == "left":
				r.rotateLeft()
			break
		time.sleep(0.01)
	r.resetPassedLine()
	r.goStraight()
	while True:
		state = passedBlackLine(r, state)
		print ("SECOND AXIS: LINES PASSED " + str(r.getLinePassed()))
		if r.getLinePassed() == numOfLines:
			r.stop()
			r.lowerForkArm()
			break


# Robot will run straight until it has met 2 black lines, then turn right and stop.
if __name__ == "__main__":

	r = robot_uppsala.EV3Robot()
	print("Waiting for connection on RFCOMM channel %d" % port)
	client_sock, client_info = server_sock.accept()
	print("Accepted connection from ", client_info)

	try:
		while True:
			data = client_sock.recv(1024)
			if len(data) == 0: break
			print("received [%s]" % data)

			numberOflines = int(data)
			try:
				r.liftForkArm()
				run(numberOflines, "right")
			except KeyboardInterrupt:
				#print(e)
				r.stop()
	# Run motor on received message
	#        m = ev3.LargeMotor('outD')
	#        n = ev3.LargeMotor('outA')
	#        m.run_timed(time_sp=100, speed_sp=-100)
	except IOError:
		pass

	print("disconnected")

client_sock.close()
server_sock.close()

