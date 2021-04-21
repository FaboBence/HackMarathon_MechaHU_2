import selectors, struct, json
from Custom_Errors import *

#test = 0

class User:
	def __init__(self,Name,RoomID):
		self.__Name = Name
		self.__RoomID = RoomID
	def get_Name(self):
		return self.__Name
	def get_RoomID(self):
		return self.__RoomID
	def set_Name(self,Name):
		self.__Name = Name
	def set_RoomID(self,RoomID):
		self.__RoomID = RoomID

class Message:
	def __init__(self, selector, socket, addr, Name, RoomID):
		self.selector = selector
		self.sock = socket
		self.addr = addr
		self.Name = Name		# Name of current User
		self.RoomID = RoomID	# ID of the Room the user is currently in
		self.Users = []			# List of User type objects
		self._recv_buffer = b""
		self._send_buffer = b""
		self._headerlen = 2 # Bytes
		self._messagelen = None

	def _set_selector_events_mask(self, mode):
		if mode == "r":
			events = selectors.EVENT_READ
		elif mode == "w":
			events = selectors.EVENT_WRITE
		elif mode == "rw":
			events = selectors.EVENT_READ | selectors.EVENT_WRITE
		self.selector.modify(self.sock, events, data = self)

	def process(self,mask):
		if mask & selectors.EVENT_READ:
			self.read()
		if mask & selectors.EVENT_WRITE:
			self.write()

	def read(self):
		print('Read ',self.Name) # DEBUG
		try:
			data = self.sock.recv(1024)
		except BlockingIOError:
			pass
		else:
			if data:
				self._recv_buffer += data
			else:
				raise ServerDisconnectError()

			# Decoding data:
			self._decode_messagelen()
			if self._messagelen is not None:
				self._decode_message()
			print(str())
			self._set_selector_events_mask("w")

	def _decode_messagelen(self):
		if len(self._recv_buffer) >= self._headerlen: # Header lenght
			self._messagelen = struct.unpack(">H", self._recv_buffer[:self._headerlen])[0]
			self._recv_buffer = self._recv_buffer[self._headerlen:]

	def _decode_message(self):
		if len(self._recv_buffer) >= self._messagelen:
			tmp = self._recv_buffer[:self._messagelen].decode('utf-8')
			self._recv_buffer = self._recv_buffer[self._messagelen:]
			msg_list = json.loads(tmp)	# received message is a list of dictionaries
			self.Users.clear()			# Clearing Users, so we can refresh them
			for msg_dict in msg_list:
				print("  ", msg_dict)
				Name = msg_dict.get("Name")
				RoomID = msg_dict.get("RoomID")
				if Name == self.Name:
					self.RoomID = RoomID
				else:
					self.Users.append(User(Name,RoomID))

	def write(self):
		#global test
		if True:#test < 3*2:
			print('Write ',self.Name) # DEBUG
			self._encode_message()
			try:
				sent = self.sock.send(self._send_buffer)
			except BlockingIOError:
				pass
			else:
				self._send_buffer = self._send_buffer[sent:]
				self._set_selector_events_mask("r")
		else:
			self.close()
		#test += 1

	def _encode_message(self):
		tmp_dict = {"Name": self.Name, "RoomID": self.RoomID}
		print("  ",tmp_dict)
		msg = json.dumps(tmp_dict, ensure_ascii=False).encode('utf-8')
		self._send_buffer += struct.pack(">H",len(msg)) + msg

	def close(self):
		print("Closing connection to ", self.addr)
		try:
			self.selector.unregister(self.sock)
			self.sock.close()
		except:
			pass
		finally:
			self.sock = None