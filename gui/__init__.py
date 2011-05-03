#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk, gtk, os
pygtk.require("2.0")
from tab_channels import GuiTabChannels

class GuiConfig:
	def __init__(self, desc, text = None, choices = None, integer = None, boolean = None, mini = None, maxi = None):
		self.tab = [desc]

		if text != None:
			self.tab.append(str(text))
			self.tab.append(choices == None)
		else:
			self.tab.append('')
			self.tab.append(False)
			
		if boolean != None:
			self.tab.append(bool(boolean))
			self.tab.append(True)
		else:
			self.tab.append(False)
			self.tab.append(False)

		ls = gtk.ListStore(str)
		if choices:
			for a in choices:
				ls.append((str(a),))
			self.tab.append(ls)
			self.tab.append(True)
		else:
			self.tab.append(ls)
			self.tab.append(False)
			
		if integer != None:
			self.tab.append(int(integer))
			self.tab.append(True)
			self.tab.append(gtk.Adjustment(value=integer, lower=mini, upper=maxi, step_incr=1))
		else:
			self.tab.append(0)
			self.tab.append(False)
			self.tab.append(gtk.Adjustment())
			
		
	def __iter__(self):
		return self.tab.__iter__()

class Gui(GuiTabChannels, object):
	def __init__(self):
		# Window loading
		self.builder = gtk.Builder()
		self.builder.add_from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.ui"))
		
		# Init tabs
		GuiTabChannels.__init__(self)
		
		# Connecting signals
		self.builder.connect_signals(self)

		# Viewing
		self.window = self.builder.get_object("w_main")
		self.window.show()
		gtk.main()

	def on_quit(self,widget=None,data=None):
		widget.show()
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, "Do you really want to quit ?")
		dialog.set_title('Closing Iris Monitor')
		response = dialog.run()
		dialog.destroy()

		if response == gtk.RESPONSE_YES:
			if self.channel:
				self.channel.thread_stop()
			gtk.main_quit()
		else:
			return True
