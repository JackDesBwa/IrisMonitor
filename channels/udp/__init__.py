#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, config, events
from channels import IrisChannel

class udp(IrisChannel):
	def __init__(self):
		IrisChannel.__init__(self)
		self.config = config.ConfigList(self.__class__, {
			'port' : config.ConfigInt('Port to listen', 0, 65535, 50000)
		})

	def run(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(('localhost', self.config.port))
		while 1:
			msg, addr = self.sock.recvfrom(1024)
			for byte in msg:
				if not byte: byte = '\x00'
				events.fire(IrisChannel, 'onReceive', byte)
