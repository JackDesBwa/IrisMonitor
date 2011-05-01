#!/usr/bin/env python

class ConfigList:
	def __init__(self, configs):
		self.__dict__['configs'] = {}
		if isinstance(configs, dict):
			for x in configs:
				if isinstance(configs[x], ConfigBase):
					self.__dict__['configs'][x] = configs[x]

	def __getattr__(self, attr):
		if attr in self.__dict__['configs']:
			return self.configs[attr].get()
		else:
			raise AttributeError()

	def __setattr__(self, attr, val):
		if attr in self.__dict__['configs']:
			self.configs[attr].set(val)
			
	def __iter__(self):
		return self.configs.keys().__iter__()

class ConfigBase:
	def get(self):
		return self.value
	
	def set(self, value):
		pass
		
	def condition(self):
		pass

class ConfigString(ConfigBase):
	def __init__(self, desc, default = ''):
		self.desc = str(desc)
		self.set(default)

	def condition(self):
		return 'a string'

	def set(self, value):
		self.value = str(value)

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

	def set(self, value):
		if str(value) in self.available:
			self.value = self.available[str(value)]

class ConfigInt(ConfigBase):
	def __init__(self, desc, mini=None, maxi=None, default=None):
		self.mini = int(mini) if mini else None
		self.maxi = int(maxi) if maxi else None
		self.desc = str(desc)
		self.value = self.mini if self.mini else self.maxi if self.maxi else 0
		if default != None:
			self.set(default)

	def condition(self):
		if self.mini != None and self.maxi != None:
			return 'between %d and %d' % (self.mini, self.maxi)
		elif self.mini != None:
			return 'less than %d' % (self.maxi)
		elif self.mini != None:
			return 'more than %d' % (self.mini)
		else:
			return 'an integer'

	def set(self, value):
		if (not self.mini or int(value) >= self.mini) and (not self. maxi or int(value) <= self.maxi):
			self.value = int(value)

class ConfigFloat(ConfigBase):
	def __init__(self, desc, mini=None, maxi=None, default=None):
		self.mini = float(mini) if mini else None
		self.maxi = float(maxi) if maxi else None
		self.desc = desc
		self.value = self.mini if self.mini else self.maxi if self.maxi else 0
		if default != None:
			self.set(default)
			
	def condition(self):
		if self.mini != None and self.maxi != None:
			return 'between %d and %d' % (self.mini, self.maxi)
		elif self.mini != None:
			return 'less than %d' % (self.maxi)
		elif self.mini != None:
			return 'more than %d' % (self.mini)
		else:
			return 'an number'

	def set(self, value):
		if (not self.mini or value >= self.mini) and (not self. maxi or value <= self.maxi):
			self.value = float(value)
