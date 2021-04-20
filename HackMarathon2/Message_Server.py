import selectors, struct
from Custom_Errors import *

test = 1

class Message:
	def __init__(self, selector, socket, addr):
		self.selector = selector
		self.sock = socket
		self.addr = addr
		self.name = None    # String
		self.roomID = None  # Int
		self._recv_buffer = b""
		self._send_buffer = b""
		self._headerlen = None
		self._datalen = None

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
		if len(self._recv_buffer) > 2: # Header lenght
			_decode_headerlen()

		self._set_selector_events_mask("w")

	def _decode_headerlen(self):
		self._headerlen = struct.unpack(">H", self._recv_buffer[:2])[0]
		print('  _headerlen: ' + str(self._headerlen) + '  from ' + repr(self.addr))  # DEBUG
		self._recv_buffer = self._recv_buffer[2:]


	def write(self):
		print('Write') # DEBUG
		self._send_buffer += struct.pack(">H",test)
		print('  Test: ' + str(test) + '  to ' + repr(self.addr))  # DEBUG
		try:
			sent = self.sock.send(self._send_buffer)
		except BlockingIOError:
			pass
		else:
			self._send_buffer = self._send_buffer[sent:]
			self._set_selector_events_mask("r")
			#if sent and not self._send_buffer:
			#	self.close()
	def close(self):
		print("Closing connection to ", self.addr)
		try:
			self.selector.unregister(self.sock)
			self.sock.close()
		except:
			pass
		finally:
			self.sock = None