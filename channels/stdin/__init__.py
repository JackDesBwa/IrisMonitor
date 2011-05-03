#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, events
from channels import IrisChannel

class stdin(IrisChannel):
	"""Using standard input"""
	def __init__(self):
		IrisChannel.__init__(self)

	def loop(self):
		byte = sys.stdin.read(1)
		if not byte: byte = '\x00'
		events.fire(IrisChannel, 'onReceive', byte)
