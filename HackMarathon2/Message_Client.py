import selectors, struct
from Custom_Errors import *

test = 0

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

	def process(self,mask):
		if mask & selectors.EVENT_READ:
			self.read()
		if mask & selectors.EVENT_WRITE:
			self.write()

	def read(self):
		global test
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

	def write(self):
		global test
		if test < 5:
			print('Write') # DEBUG
			self._send_buffer += struct.pack(">H",test+1)
			print('  Writing: ' + str(test+1) + '  '+ repr(self.addr))  # DEBUG
			try:
				sent = self.sock.send(self._send_buffer)
			except BlockingIOError:
				pass
			else:
				self._send_buffer = self._send_buffer[sent:]
				self._set_selector_events_mask("r")
		else:
			self.close()


	def close(self):
		print("Closing connection to ", self.addr)
		try:
			self.selector.unregister(self.sock)
			self.sock.close()
		except:
			pass
		finally:
			self.sock = None