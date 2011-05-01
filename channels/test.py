#!/usr/bin/env python

import sys, os
sys.path.remove(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import channels, config, events

onReceive_col = 0
def onReceive(event, byte):
	global onReceive_col
	if not byte : return
	onReceive_col += 1
	sys.stdout.write("0x%02X" % ord(byte))
	if ord(byte) > 31 and ord(byte) < 127:
		sys.stdout.write("(")
		sys.stdout.write(byte)
		sys.stdout.write(") ")
	else :
		sys.stdout.write("    ")
	if onReceive_col == 8:
		onReceive_col = 0
		sys.stdout.write("\n")

events.register(channels.IrisChannel, 'onReceive', onReceive)
sys.stdout.write('Available channels are :\n')
i = 0
chanlist = channels.get_list()
for c in chanlist:
	sys.stdout.write('  %3d    %s\n' % (i, c))
	i += 1

sys.stdout.write('Which one would be tested ? ')

try:
	a = int(sys.stdin.readline())
	theclass = channels.get_class(chanlist[a])
except ValueError:
	sys.exit('Invalid number.\n')
except IndexError:
	sys.exit('Unknowed entry.\n')
except KeyboardInterrupt:
	sys.exit('Interrupted test.\n')

sys.stdout.write('Test of `%s`\n' % chanlist[a])
chan = theclass()

sys.stdout.write('\nYou should probably change the configuration.\nType `c` to modify a parameter or anything else if you accept the value :')
try:
	config_list = chan.get_config_list()
	for c in config_list:
		validated = False;
		while not validated:
			sys.stdout.write('\n`%s` is set to `%s`        ' % (c, getattr(config_list, c)))
			if sys.stdin.readline() == 'c\n':
				sys.stdout.write('    You want to change the value of `%s`. Type the new value.\n    ' % c)
				sys.stdout.write('The value should be %s.\n    ' % config_list.configs[c].condition())
						
				setattr(config_list, c, sys.stdin.readline().strip())
			else:
				validated = True
except KeyboardInterrupt:
	sys.exit('Interrupted test.\n')
sys.stdout.write('OK. All parameters are set.\n')

try:
	chan.run()
except KeyboardInterrupt:
	sys.stdout.write('End of test.\n')
