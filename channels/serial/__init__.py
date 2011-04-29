#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config, events
from channels import IrisChannel
try:
	import serial as rs232

	class serial(IrisChannel):
		def __init__(self):
			# TODO : Configuration
			self.serial = rs232.Serial('./virtual_tty', baudrate=38400, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0, rtscts=0)
				

		def run(self):
			while 1:
				events.fire(IrisChannel, 'onReceive', self.serial.read(1))
except:
	pass
