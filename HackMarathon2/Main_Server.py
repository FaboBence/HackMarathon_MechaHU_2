import socket, struct, selectors, Message_Server

def accept_connection(sock):
	conn, addr = sock.accept()
	conn.setblocking(False)
	events = selectors.EVENT_WRITE | selectors.EVENT_READ
	message = Message_Server.Message(sel, conn, addr)
	sel.register(conn, events, data=message)

sel = selectors.DefaultSelector()

host, port = ['127.0.0.1', 65432]
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
	while True:
		events = sel.select(timeout = None)
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
