#!/usr/bin/env python

assoc = {}

def register(eventgroup, event, fct):
	global assoc
	if not assoc.has_key(eventgroup):
		assoc[eventgroup] = {}
	if not assoc[eventgroup].has_key(event):
		assoc[eventgroup][event] = []
	assoc[eventgroup][event].append(fct)

def fire(eventgroup, event, value):
	global assoc
	if assoc.has_key(eventgroup):
		if assoc[eventgroup].has_key(event):
			for fct in assoc[eventgroup][event]:
				fct(value)
