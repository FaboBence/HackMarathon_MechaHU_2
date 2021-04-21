import socket, selectors, Message_Client
from Custom_Errors import *

def start_connection(host,port):
    addr = (host, port)
    names = ["Bence","Misi","Gellert"]
    for name in names:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)  # Connecting to server
        print("Connecting to: " + repr(addr))
        events = selectors.EVENT_WRITE #| selectors.EVENT_READ
        message = Message_Client.Message(sel, sock, addr, Name=name,RoomID=0)
        sel.register(sock, events, data=message)

sel = selectors.DefaultSelector()
host, port = ['127.0.0.1', 65432]
start_connection(host, port)

try:
    while True:
        print("Waiting for events = sel.select()")
        events = sel.select(timeout=1)
        for key, mask in events:
            message = key.data
            try:
                message.process(mask)
            except ServerDisconnectError:
                print("Server closed connection.")
                message.close()
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