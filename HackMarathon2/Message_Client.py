import selectors, struct, json
from Custom_Errors import *

test = 0

class Message:
	def __init__(self, selector, socket, addr, Name, RoomID):
		self.selector = selector
		self.sock = socket
		self.addr = addr
		self.Name = Name
		self.RoomID = RoomID
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
		print('Read') # DEBUG
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
			test = struct.unpack(">H", self._recv_buffer[:2])[0]
			print('  Test: ' + str(test) + '  '+ repr(self.addr)) #+ '  _recv_buffer: ' + repr(self._recv_buffer))  # DEBUG
			self._recv_buffer = self._recv_buffer[2:]
			self._set_selector_events_mask("w")

	def _decode_messagelen(self):
		if len(self._recv_buffer) >= self._headerlen: # Header lenght
			self._messagelen = struct.unpack(">H", self._recv_buffer[:self._headerlen])[0]
			self._recv_buffer = self._recv_buffer[self._headerlen:]
# Still has to change
	def _decode_message(self):
		if len(self._recv_buffer) >= self._messagelen:
			tmp = self._recv_buffer[:self._messagelen].decode('utf-8')
			self._recv_buffer = self._recv_buffer[self._messagelen:]
			msg_dict = json.loads(tmp) # received data in dictionary
			if msg_dict.get("Name") is not None:
				self.Name = msg_dict.get("Name")
			if msg_dict.get("RoomID") is not None:
				self.RoomID = msg_dict.get("RoomID")

	def write(self):
		global test
		if test < 5:
			print('Write') # DEBUG
			_encode_message()
			try:
				sent = self.sock.send(self._send_buffer)
			except BlockingIOError:
				pass
			else:
				self._send_buffer = self._send_buffer[sent:]
				self._set_selector_events_mask("r")
		else:
			self.close()

	def _encode_message(self):
		tmp_dict = {"Name": self.name, "RoomID": self.RoomID}
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