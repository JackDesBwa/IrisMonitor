#!/usr/bin/env python

import config
from threading import Thread

class IrisChannel:
	def __init__(self):
		self.stop_running = True
		self.config = config.ConfigList(self.__class__, ());
	
	def get_config_list(self):
		return self.config

	def start(self, wait = False):
		self.thread = Thread(target=self.thread_run)
		self.thread.start()
		if wait:
			self.thread.join()
	
	def thread_run(self):
		self.stop_running = False
		self.loop_init()
		while not self.stop_running:
			self.loop()
		self.loop_finish()
			
	def thread_stop(self, cb = None):
		if not self.stop_running:
			self.stop_running = True
			self.thread.join(5)
			if self.thread.is_alive():
				self.thread._Thread__stop()
		if cb:
			cb()

	def stop(self, cb = None):
		Thread(target=self.thread_stop, args=(cb,)).start()
			

	def loop_init(self):
		pass

	def loop(self):
		pass

	def loop_finish(self):
		pass

import os, sys

def get_list():
	return list(plugin_list.keys())

def get_class(plugin):
	pluginpath = os.path.abspath(os.path.dirname(__file__))
	if not pluginpath in sys.path:
		sys.path.append(pluginpath)
	if plugin in plugin_list:
		return plugin_list[plugin]

plugin_list = {}
pluginpath = os.path.abspath(os.path.dirname(__file__))
if pluginpath:
	for plugin in os.listdir(pluginpath):
		directory = os.path.join(pluginpath, plugin)
		if os.path.isdir(directory):
			if os.path.exists(os.path.join(directory, '__init__.py')):
				imported = __import__(plugin, globals(), locals(), (plugin))
				if plugin in imported.__dict__:
					theclass = imported.__dict__[plugin]
					if issubclass(theclass, IrisChannel):
						plugin_list[plugin] = theclass
