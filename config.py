#!/usr/bin/env python

class Config(object):
	instance = None
	def __new__(c):
		if not Config.instance:
			Config.instance = Config.__Config()
		return Config.instance
	def __getattr__(self, attr):
		return getattr(self.instance, attr)
	def __setattr__(self, attr, val):
		return setattr(self.instance, attr, val)
	class __Config:
		def __init__(self):
			self.val = None
		def __str__(self):
			return `self` + self.val
