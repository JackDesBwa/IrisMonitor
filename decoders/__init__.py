#!/usr/bin/env python

class IrisDecoder:
	def decode(self, byte):
		return None

import os, sys

def get_list():
	return plugin_list.keys()

def get_class(plugin):
	pluginpath = os.path.abspath(os.path.dirname(__file__))
	if not pluginpath in sys.path:
		sys.path.append(pluginpath)
	if plugin in plugin_list:
		imported = __import__(plugin, globals(), locals(), (plugin))
		return imported.__dict__[plugin]

plugin_list = {}
pluginpath = os.path.abspath(os.path.dirname(__file__))
if pluginpath:
	for plugin in os.listdir(pluginpath):
		directory = os.path.join(pluginpath, plugin)
		if os.path.isdir(directory):
			if os.path.exists(os.path.join(directory, '__init__.py')):
				imported = __import__(plugin, globals(), locals(), (plugin))
				theclass = imported.__dict__[plugin]
				if issubclass(theclass, IrisDecoder):
					plugin_list[plugin] = theclass
