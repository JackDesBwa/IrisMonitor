#!/usr/bin/env python
# -*- coding: utf-8 -*-

import channels, gtk, os, json

class GuiTabChannels:
	def __init__(self):
		# Current channel
		self.channel = None
		
		# Default config
		try:
			configfile = open(os.path.expanduser('~/.irismonitor/default_channel.json'))
			jsondata = configfile.read()
			self.channel = eval(json.loads(jsondata)[0] + '()')
			self.channel.get_config_list().load(jsondata)
			configfile.close()
		except IOError:
			pass
		
		# Available channels
		index = None
		i = 0
		ls_channels = self.builder.get_object("ls_channels")
		chans = channels.get_list()
		for x in chans:
			ls_channels.append((x, channels.get_class(x).__doc__))
			if self.channel and x == self.channel.__class__.__name__:
				index = i
			i += 1
		
		if index:
			widget = self.builder.get_object("combo_channels")
			widget.set_active(index)
			self.on_channel_change(widget)

	def update_channel_config_list(self):
		ls_channels_config = self.builder.get_object('ls_channels_config')
		ls_channels_config.clear()
		config_list = self.channel.get_config_list()
		for c in config_list:
			li = [c]
			li.extend(config_list.configs[c].gui_config())
			ls_channels_config.append(li)

	def on_channel_change(self,widget=None,data=None):
		if self.channel: 
			self.channel.stop()
		self.builder.get_object('btn_channels_start').set_sensitive(True)
		self.builder.get_object('btn_channel_defsave').set_sensitive(True)
		self.builder.get_object('btn_channel_save').set_sensitive(True)
		self.builder.get_object('btn_channel_load').set_sensitive(True)
		ls_channels = self.builder.get_object('ls_channels')
		self.channel = channels.get_class(ls_channels.get_value(widget.get_active_iter(), 0))()
		self.update_channel_config_list()

	def on_channel_start(self,widget=None,data=None):
		self.builder.get_object('combo_channels').set_sensitive(False)
		self.builder.get_object('tv_channels_config').set_sensitive(False)
		self.builder.get_object('btn_channels_start').set_sensitive(False)
		self.builder.get_object('btn_channel_load').set_sensitive(False)
		self.builder.get_object('btn_channels_stop').set_sensitive(True)
		self.channel.start()


	def on_channel_stop(self,widget=None,data=None):
		self.builder.get_object('btn_channels_stop').set_sensitive(False)
		self.channel.stop(self.on_channel_stopped)

	def on_channel_stopped(self):
		self.builder.get_object('btn_channel_load').set_sensitive(True)
		self.builder.get_object('btn_channels_start').set_sensitive(True)
		self.builder.get_object('tv_channels_config').set_sensitive(True)
		self.builder.get_object('combo_channels').set_sensitive(True)

	def on_channel_config_change(self,widget=None, row=None ,data=None):
		ls_channels_config = self.builder.get_object('ls_channels_config')
		option = ls_channels_config[row][0]
		value = ls_channels_config[row][6].get(data, 0)[0] if isinstance(data, gtk.TreeIter) else data
		if str(getattr(self.channel.get_config_list(), option)) != str(value):
			setattr(self.channel.get_config_list(), option, value)
			self.update_channel_config_list()

	def on_channel_setdefault(self,widget=None,data=None):
		if not os.path.isdir(os.path.expanduser('~/.irismonitor/')):
			os.makedirs(os.path.expanduser('~/.irismonitor/'))
		configfile = open(os.path.expanduser('~/.irismonitor/default_channel.json'), 'w')
		configfile.write(unicode(self.channel.get_config_list().save()))
		configfile.close()

	def on_channel_save(self,widget=None,data=None):
		chooser = gtk.FileChooserDialog(title='Save configuration', action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		chooser.set_current_name('myconfig.%s.channel.json' % self.channel.__class__.__name__)
		filefilter = gtk.FileFilter()
		filefilter.set_name('Channel %s' % self.channel.__class__.__name__)
		filefilter.add_pattern('*.%s.channel.json' % self.channel.__class__.__name__)
		chooser.add_filter(filefilter)
		filefilter = gtk.FileFilter()
		filefilter.set_name("All files")
		filefilter.add_pattern("*")
		chooser.add_filter(filefilter)
		response = chooser.run()
		if response == gtk.RESPONSE_OK:
			configfile = open(chooser.get_filename(), 'w')
			configfile.write(unicode(self.channel.get_config_list().save()))
			configfile.close()
		chooser.destroy()
		
	def on_channel_load(self,widget=None,data=None):
		chooser = gtk.FileChooserDialog(title='Open configuration', action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		chooser.set_filename('myconfig.%s.channel.json' % self.channel.__class__.__name__)
		filefilter = gtk.FileFilter()
		filefilter.set_name('Channel %s' % self.channel.__class__.__name__)
		filefilter.add_pattern('*.%s.channel.json' % self.channel.__class__.__name__)
		chooser.add_filter(filefilter)
		filefilter = gtk.FileFilter()
		filefilter.set_name("All files")
		filefilter.add_pattern("*")
		chooser.add_filter(filefilter)
		response = chooser.run()
		if response == gtk.RESPONSE_OK:
			configfile = open(chooser.get_filename())
			self.channel.get_config_list().load(configfile.read())
			configfile.close()
		chooser.destroy()
		self.update_channel_config_list()
