import selectors, struct, json
from Custom_Errors import *

class Message:
	def __init__(self, selector, socket, addr):
		self.selector = selector
		self.sock = socket
		self.addr = addr
		self.Name = None    # String
		self.roomID = None  # Int
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

	def process(self, mask):
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
				raise ClientDisconnectError()
			# Decoding data:
			_decode_messagelen()
			if self._messagelen is not None:
				_decode_message()
			self._set_selector_events_mask("w")

	def _decode_messagelen(self):
		if len(self._recv_buffer) >= self._headerlen: # Header lenght
			self._messagelen = struct.unpack(">H", self._recv_buffer[:self._headerlen])[0]
			self._recv_buffer = self._recv_buffer[self._headerlen:]

	def _decode_message(self):
		if len(self._recv_buffer) >= self._messagelen:
			tmp = self._recv_buffer[:self._messagelen].decode('utf-8')
			self._recv_buffer = self._recv_buffer[self._messagelen:]
			msg_dict = json.loads(tmp) # received data in dictionary
			if msg_dict.get("Name") is not None:
				self.Name = msg_dict.get("Name")
			if msg_dict.get("RoomID") is not None:
				self.roomID = msg_dict.get("RoomID")

	def write(self):
		print('Write') # DEBUG
		self._send_buffer += struct.pack(">H",test)
		try:
			sent = self.sock.send(self._send_buffer)
		except BlockingIOError:
			pass
		else:
			self._send_buffer = self._send_buffer[sent:]
			self._set_selector_events_mask("r")

	def close(self):
		print("Closing connection to ", self.addr)
		try:
			self.selector.unregister(self.sock)
			self.sock.close()
		except:
			pass
		finally:
			self.sock = None