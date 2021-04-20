import socket, struct, selectors, Message_Server, time
from Custom_Errors import *

def accept_connection(sock):
	conn, addr = sock.accept()
	print("Connecting to: " + repr(addr))
	conn.setblocking(False)
	events = selectors.EVENT_READ #| selectors.EVENT_WRITE
	message = Message_Server.Message(sel, conn, addr)
	sel.register(conn, events, data=message)

sel = selectors.DefaultSelector()

host, port = ['127.0.0.1', 65432]
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
	while True:
		t = 0	# For timeout
		print("Waiting for events = sel.select()")
		while t < 0.2: # Always waiting for response
			start = time.time()
			events = sel.select(timeout = 0.11)
			t += time.time() - start
		# If someone didn't answer
		#map = sel.get_map()
		#for i in map:
		#	if map[i].data is not None and (map[i],selectors.EVENT_READ) not in events:
		#		print("Ping wasn't sent")
		#		map[i].data.close()

		for key, mask in events:
			if key.data is None:
				accept_connection(key.fileobj)
			else:
				message = key.data
				try:
					message.process(mask)
				except ClientDisconnectError:
					print("Client closed connection.")
					message.close()
				except:
					print("Something went wrong with 'message.process(mask)'")
					message.close()

except KeyboardInterrupt:
	print("Exiting.")
finally:
	sel.close()
