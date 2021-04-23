import socket, struct, selectors, Message_Server, time
from Custom_Errors import *
import Office_allocation

def accept_connection(sock):
	conn, addr = sock.accept()
	#print("Connecting to: " + repr(addr))
	conn.setblocking(False)
	events = selectors.EVENT_READ #| selectors.EVENT_WRITE
	message = Message_Server.Message(sel, conn, addr, Name_Room_dict)
	sel.register(conn, events, data=message)
def print_schedule(Week_schedule, Week_matrix):
	print()
	print("--------------------------------------")
	for i in range(len(Week_matrix)):
		if i==0:
			print("Monday")
		if i==1:
			print("Tuesday")
		if i==2:
			print("Wednesday")
		if i==3:
			print("Thursday")
		if i==4:
			print("Friday")
		print("              8       9      10      11      12      13      14      15      16      17")
		for j in range(len(Week_matrix[i])):
			personal_schedule=[]
			for col in range(Week_schedule[i].shape[1]):
				present=False
				for row in range(Week_schedule[i].shape[0]):
					if Week_schedule[i][row][col]==Week_matrix[i][j][0]:
						personal_schedule.append("No."+str(row))
						present=True
				if present==False:
					personal_schedule.append("Home")

			
			print("{0:^10}".format(Week_matrix[i][j][1]),end='')
			print(personal_schedule)
			print()
		print("--------------------------------------")
		print()
# Creating schedule
day = 4 # Monday: 0, Tuesday: 1, Wednesday: 2, Thursday: 3, Friday: 4
hour = 17
Week_Schedule, dataframe,Week_matrix = Office_allocation.office_allocation()
print_schedule(Week_Schedule,Week_matrix)
dataframe = dataframe.to_numpy()
Name_Room_dict = {}
for i,room in enumerate(Week_Schedule[day]):
	reg_id = room[hour-9] # Id of User in room
	if reg_id != -1:
		Name = dataframe[reg_id][0]
		Name_Room_dict.update([(Name,i)])
#print(Name_Room_dict)
#Name_Room_dict = {"Misi":1,"Gellert":2,"Bence":3}

# Setting up server
limit = 1 # Timeout [seconds]
sel = selectors.DefaultSelector()
host, port = ['127.0.0.1', 65432]
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
#print("Listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
	while True:
		t = 0	# For measuring timeout
		#print("Waiting for events = sel.select()")
		while t < limit: # Always waiting for response
			start = time.time()
			events = sel.select(timeout = limit/2+0.01)
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
					#print("Client closed connection.")
					message.close()
				except:
					#print("Something went wrong with 'message.process(mask)'")
					message.close()

except KeyboardInterrupt:
	#print("Exiting.")
	pass
finally:
	sel.close()
