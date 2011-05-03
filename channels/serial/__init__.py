#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config, events
from channels import IrisChannel
try:
	import serial as serial_module

	class serial(IrisChannel):
		"""Using serial port (COM/RS232/TTY)"""
		def __init__(self):
			IrisChannel.__init__(self)
			self.config = config.ConfigList(self.__class__, {
				'port' : config.ConfigString('Port name', '0'),
				'baudrate' : config.ConfigChoice('Baudrate', serial_module.Serial.BAUDRATES, 9600),
				'bytesize' : config.ConfigInt('Size of each byte', 5, 8, 8),
				'parity' : config.ConfigChoice('Parity', {'None':serial_module.PARITY_NONE, 'Odd':serial_module.PARITY_ODD, 'Even':serial_module.PARITY_EVEN, 'Mark':serial_module.PARITY_MARK, 'Space':serial_module.PARITY_SPACE}, 'None'),
				'stopbits' : config.ConfigInt('Number of stop bits', 1, 2),
				'control' : config.ConfigChoice('Flow control method', ('None', 'RTS/CTS', 'Xon/Xoff'), 'None')
			})

		def loop_init(self):
			xonxoff = rtscts = False
			if self.config.control == 'RTS/CTS':
				rtscts = True
			elif self.config.control == 'Xon/Xoff':
				xonxoff = True
			self.serial = serial_module.Serial(self.config.port, baudrate=self.config.baudrate, bytesize=self.config.bytesize, parity=self.config.parity, stopbits=self.config.stopbits, timeout=None, xonxoff=xonxoff, rtscts=rtscts)

		def loop(self):
			events.fire(IrisChannel, 'onReceive', self.serial.read(1))

		def loop_finish(self):
			self.serial.close()
except:
	sys.stderr.write('`pyserial` is needed for using the serial channel.')
	pass
