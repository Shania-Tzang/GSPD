from bluetooth import *
import sys
import time
import robot

# Setup Bluetooth socket
def setupBluetooth():
	server_sock=BluetoothSocket( RFCOMM )
	server_sock.bind(("",PORT_ANY))
	server_sock.listen(1)


	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

	advertise_service( server_sock, "SampleServer",
					   service_id = uuid,
					   service_classes = [ uuid, SERIAL_PORT_CLASS ],
					   profiles = [ SERIAL_PORT_PROFILE ],)
	#                   protocols = [ OBEX_UUID ]
	return server_sock


def rerun():
	try:
		while True:
			# data = client_sock.recv(1024)
			data = client_sock.recv(10).decode()
			if len(data) == 0: break
			print("received: %s" % data)

			parsedY = int(data[0])
			parsedX = int(data[1])
			# client_sock.send("ok\n")

			r.setBeginPos([1, 1])
			r.setDesPos([parsedY, parsedX])
			r.setOrientation([1, 0])
			r.raiseArm()
			r.deliver()
	except KeyboardInterrupt:
		# print("s")
		r.stop()
		running = False
	except IOError:
		pass



# Robot get destination, go to it, then lower the cargo, move back a bit, then return to starting position
if __name__ == "__main__":

	server_sock = setupBluetooth()
	port = server_sock.getsockname()[1]

	print("Waiting for connection on RFCOMM channel %d" % port)
	client_sock, client_info = server_sock.accept()
	print("Accepted connection from ", client_info)

	#while True:
	data = client_sock.recv(512).decode()
	#if data == "done": break
	print("received: %s" % data)
	package_requirements = data

	client_sock.close()
	server_sock.close()

	time.sleep(1)
	server_sock = setupBluetooth()

	print("Waiting for connection on RFCOMM channel %d" % port)
	client_sock, client_info = server_sock.accept()
	print("Accepted connection from ", client_info)

	client_sock.send(str(package_requirements) + "\n")
	print("done")
	r = robot.EV3Robot(client_sock)
	running = True
	try:
		while running:
			#data = client_sock.recv(1024)
			data = client_sock.recv(10).decode()
			if len(data) == 0: break
			print("received: %s" % data)

			parsedY = int(data[0])
			parsedX = int(data[1])
			#client_sock.send("ok\n")

			r.setBeginPos([1,1])
			r.setDesPos([parsedY, parsedX])
			r.setOrientation([1,0])
			r.raiseArm()
			r.deliver()
			inputMsg = input("rerun?:")
			if (inputMsg == "y"):
				rerun()

	except KeyboardInterrupt:
		#print("s")
		r.stop()
		running = False
	except IOError:
		pass

	print("disconnected")

	client_sock.close()
	server_sock.close()

