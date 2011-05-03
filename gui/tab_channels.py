#!/usr/bin/env python
# -*- coding: utf-8 -*-

import channels, gtk

class GuiTabChannels:
	def __init__(self):
		# Current channel
		self.channel = None
		
		# Available channels
		ls_channels = self.builder.get_object("ls_channels")
		chans = channels.get_list()
		for x in chans:
			ls_channels.append((x, channels.get_class(x).__doc__))
	
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
		ls_channels = self.builder.get_object('ls_channels')
		self.channel = channels.get_class(ls_channels.get_value(widget.get_active_iter(), 0))()
		self.update_channel_config_list()

	def on_channel_start(self,widget=None,data=None):
		self.builder.get_object('combo_channels').set_sensitive(False)
		self.builder.get_object('tv_channels_config').set_sensitive(False)
		self.builder.get_object('btn_channels_start').set_sensitive(False)
		self.builder.get_object('btn_channels_stop').set_sensitive(True)
		self.channel.start()


	def on_channel_stop(self,widget=None,data=None):
		self.builder.get_object('btn_channels_stop').set_sensitive(False)
		self.channel.stop(self.on_channel_stopped)

	def on_channel_stopped(self):
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
