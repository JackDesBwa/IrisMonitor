#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, events
from channels import IrisChannel

class stdin(IrisChannel):
	def __init__(self):
		IrisChannel.__init__(self)

	def run(self):
		while 1:
			byte = sys.stdin.read(1)
			if not byte: byte = '\x00'
			events.fire(IrisChannel, 'onReceive', byte)
