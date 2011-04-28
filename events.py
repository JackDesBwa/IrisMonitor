#!/usr/bin/env python

assoc = {}

def register(fct, event):
	global assoc
	if not assoc.has_key(event):
		assoc[event] = []
	assoc[event].append(fct)

def fire(event, time, value):
	global assoc
	if assoc.has_key(event):
		for fct in assoc[event]:
			fct(time, value)
