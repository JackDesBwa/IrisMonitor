#!/usr/bin/env python

assoc = {}
assoc_all = {}

def register_all(eventgroup, fct):
	global assoc_all
	if eventgroup not in assoc_all:
		assoc_all[eventgroup] = []
	assoc_all[eventgroup].append(fct)

def register(eventgroup, event, fct):
	global assoc
	if eventgroup not in assoc:
		assoc[eventgroup] = {}
	if event not in assoc[eventgroup]:
		assoc[eventgroup][event] = []
	assoc[eventgroup][event].append(fct)

def fire(eventgroup, event, value):
	global assoc, assoc_all
	if eventgroup in assoc:
		if event in assoc[eventgroup]:
			for fct in assoc[eventgroup][event]:
				fct(event, value)
	if eventgroup in assoc_all:
		for fct in assoc_all[eventgroup]:
			fct(event, value)
