#!/usr/bin/env python

import json, gui

class ConfigList:
	def __init__(self, name, configs):
		self.__dict__['name'] = str(name)
		self.__dict__['configs'] = {}
		if isinstance(configs, dict):
			for x in configs:
				if isinstance(configs[x], ConfigBase):
					self.__dict__['configs'][x] = configs[x]

	def get(self, attr, text = True):
		if attr in self.__dict__['configs']:
			return self.configs[attr].get(text)
		else:
			raise AttributeError()

	def __getattr__(self, attr):
		return self.get(attr, False)

	def __setattr__(self, attr, val):
		if attr in self.__dict__['configs']:
			self.configs[attr].set(val)
			
	def __iter__(self):
		return self.configs.keys().__iter__()
		
	def load(self, jsondata):
		build_struct = json.loads(jsondata)
		if build_struct[0] != self.name: return
		for key in build_struct[1]:
			setattr(self, key, build_struct[1][key])
		
	def save(self):
		build_struct = {}
		for config in self.configs:
			build_struct[config] = self.configs[config].get(True)
		build_struct = (self.name, build_struct)	
		return json.JSONEncoder(sort_keys = True, indent = 2).encode(build_struct)

class ConfigBase:
	def get(self, text = False):
		return self.value
	
	def set(self, value):
		pass
		
	def condition(self):
		pass

	def gui_config(self):
		return gui.GuiConfig('Error')

class ConfigString(ConfigBase):
	def __init__(self, desc, default = ''):
		self.desc = str(desc)
		self.set(default)

	def condition(self):
		return 'a string'

	def set(self, value):
		self.value = str(value)

	def gui_config(self):
		return gui.GuiConfig(self.desc, text = self.value)

class ConfigChoice(ConfigBase):
	def __init__(self, desc, choices, default = None):
		self.desc = str(desc)
		self.available = {}
		if isinstance(choices, dict):
			for x in choices:
				self.available[str(x)] = choices[x]
		else:
			for x in choices:
				self.available[str(x)] = x
		self.value = self.available.items()[0][1]
		self.set(default)

	def condition(self):
		return 'in ' + str(self.available.keys())
		
	def get(self, text = False):
		if not text :
			return self.value
		for x in self.available:
			if self.available[x] == self.value:
				return x

	def set(self, value):
		if str(value) in self.available:
			self.value = self.available[str(value)]

	def gui_config(self):
		return gui.GuiConfig(self.desc, text = self.get(True), choices = self.available)

class ConfigInt(ConfigBase):
	def __init__(self, desc, mini=None, maxi=None, default=None):
		self.mini = int(mini) if mini != None else None
		self.maxi = int(maxi) if maxi != None else None
		self.desc = str(desc)
		self.value = self.mini if self.mini else self.maxi if self.maxi else 0
		if default != None:
			self.set(default)

	def condition(self):
		if self.mini != None and self.maxi != None:
			return 'between %d and %d' % (self.mini, self.maxi)
		elif self.maxi != None:
			return 'less than %d' % (self.maxi)
		elif self.mini != None:
			return 'more than %d' % (self.mini)
		else:
			return 'an integer'

	def set(self, value):
		if (not self.mini or int(value) >= self.mini) and (not self. maxi or int(value) <= self.maxi):
			self.value = int(value)

	def gui_config(self):
		return gui.GuiConfig(self.desc, integer = self.value, mini = self.mini, maxi = self.maxi)

class ConfigBool(ConfigBase):
	def __init__(self, desc, default = False):
		self.value = False
		self.set(default)

	def condition(self):
		return 'a boolean'

	def set(self, value):
		self.value = True if value else False

	def gui_config(self):
		return gui.GuiConfig(self.desc, boolean = self.value)
