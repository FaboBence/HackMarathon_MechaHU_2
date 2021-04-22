import socket, selectors, threading
import tkinter as tk
import Message_Client, gui
from Custom_Errors import *

def start_connection(host,port,name):
    addr = (host, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)  # Connecting to server
    print("Connecting to: " + repr(addr))
    events = selectors.EVENT_WRITE
    message = Message_Client.Message(sel, sock, addr, Name=name,RoomID=0)
    sel.register(sock, events, data=message)

def Client_loop(main_window):
    while True:
        #print("Waiting for events = sel.select()")
        print(main_window.my_position())
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
            sel.close()
            break
    #root.after(500,Client_loop)



        ######## PROGRAM STARTS HERE #########
if __name__ == '__main__':
    input_form = tk.Tk() #Starting a form where we ask for the name of the user
    input_window = gui.name_input_window(input_form)
    input_window.pack()
    input_form.mainloop()
    name = input_window.name
    del input_form #We dont need it anymore
    if name is not None:
# Connecting to server
        sel = selectors.DefaultSelector()
        host, port = ['127.0.0.1', 65432]
        start_connection(host, port, name)
        root = tk.Tk() #Starting the main application
        mainWindow = gui.window(root, name)
        mainWindow.pack()
        #root.after(1,Client_loop)
        Client_thread = threading.Thread(target = Client_loop, args=(mainWindow,)).start()
        root.mainloop()