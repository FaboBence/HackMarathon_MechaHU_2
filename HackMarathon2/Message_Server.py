import selectors, struct

test = 1

class Message:
	def __init__(self, selector, socket, addr):
		self.selector = selector
		self.sock = socket
		self.addr = addr
		self._recv_buffer = b""
		self._send_buffer = b""

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
				raise RuntimeError("Client closed.")
			# Decoding data:
			test = struct.unpack(">H", self._recv_buffer[:2])[0]
			print('Test: ' + str(test))  # DEBUG
			self._recv_buffer = self._recv_buffer[2:]
			self._set_selector_events_mask("w")

	def write(self):
		print('Write') # DEBUG
		self._send_buffer += struct.pack(">H",test)
		try:
			sent = self.sock.send(self._send_buffer)
		except BlockingIOError:
			pass
		else:
			self._send_buffer = self._send_buffer[sent:]
			if sent and not self._send_buffer:
				self.close()
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