#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, events
from channels import IrisChannel

class udp(IrisChannel):
	def __init__(self):
		# TODO : Configuration
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(('localhost', 50000))

	def run(self):
		while 1:
			msg, addr = self.sock.recvfrom(1024)
			for byte in msg:
				if not byte: byte = '\x00'
				events.fire(IrisChannel, 'onReceive', byte)
