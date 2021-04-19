import socket, selectors, Message_Client

sel = selectors.DefaultSelector()

host, port = ['127.0.0.1', 65432]
addr = (host, port)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setblocking(False)
sock.connect_ex(addr)
events = selectors.EVENT_READ | selectors.EVENT_WRITE
message = Message_Client.Message(sel, sock, addr)
sel.register(sock, events, data=message)

try:
    while True:
        events = sel.select(timeout=1)
        for key, mask in events:
            message = key.data
            try:
                message.process(mask)
            except Exception:
                print("Something went wrong with 'message.process(mask)'")
                message.close()
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("Exiting.")
finally:
    sel.close()