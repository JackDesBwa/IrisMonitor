#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct, sys, time
import config, events
from channels import IrisChannel
from decoders import IrisDecoder

class backabackbsd(IrisDecoder):
	def __init__(self):
		self.rawdata = ''
		self.id = 0
		self.btr = 0
		self.t0 = time.time()
		self.time = 0
		events.register(IrisChannel, 'onReceive', self.decode)

	def find_id(self, c):
		self.id = hex(ord(c))
		# TODO : Messages configuration
		messages = {
			'0x42':{
				'format' : '>fff',
				'names' : ['MSG42_1', 'MSG42_2', 'MSG42_3']
			}
		}
		if self.id in messages:
			self.format = str(messages[self.id]['format']) ##
			self.names = messages[self.id]['names'] ##
			if 'scale' in messages[self.id]:
				self.scale = messages[self.id]['scale'] ##
			else:
				self.scale = [1] * len(messages[self.id]['names'])
			self.btr = struct.calcsize(self.format) + 2 ##
			self.time = time.time() - self.t0
			return True
		return False

	def checksum(self, message):
		checksum = 0
		for cc in message:
			if (checksum & 1) != 0: checksum = (checksum >> 1) + 0x8000
			else: checksum = checksum >> 1
			checksum = (checksum + ord(cc)) & 0xffff
		return checksum

	def decode(self, event, c):
		while True:
			# ID search
			if not self.btr:
				i = 0
				for cc in self.rawdata:
					i += 1
					if self.find_id(cc):
						self.rawdata = self.rawdata[i:]
						self.btr -= len(self.rawdata)
						break
					else:
						sys.stderr.write('Unknowed ID `0x%02X`\n' % ord(cc))
			
			if not self.btr:
				if not self.find_id(c):
					sys.stderr.write('Unknowed ID `0x%02X`\n' % ord(c))
				return

			# Data read
			self.rawdata += c
			self.btr -= 1
			
			# Checksum check
			if self.btr < 1:
				checksum = self.checksum(chr(int(self.id, 0)) + self.rawdata[:struct.calcsize(self.format)])
				if struct.unpack('>H', self.rawdata[struct.calcsize(self.format):struct.calcsize(self.format)+2])[0] == checksum:
					# Handling
					a = struct.unpack(self.format, self.rawdata[0:struct.calcsize(self.format)])
					for i in xrange(len(a)):
						events.fire(IrisDecoder, self.names[i], (self.time, a[i]*self.scale[i]))
					self.rawdata = self.rawdata[struct.calcsize(self.format)+2:]
				else:
					sys.stderr.write('Wrong checksum for a message of ID `%s` (%d != %d)\n' % (self.id, struct.unpack('>H', self.rawdata[struct.calcsize(self.format):struct.calcsize(self.format)+2])[0], checksum))
				self.btr = 0
			return
