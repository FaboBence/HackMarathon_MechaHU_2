import socket, struct, selectors, Message_Server

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
		print("Waiting for events = sel.select()")
		events = sel.select(timeout = None)
		print(events[0][1])
		for key, mask in events:
			if key.data is None:
				accept_connection(key.fileobj)
			else:
				message = key.data
				try:
					message.process(mask)
				except:
					print("Something went wrong with 'message.process(mask)'")
					message.close()

except KeyboardInterrupt:
	print("Exiting.")
finally:
	sel.close()
