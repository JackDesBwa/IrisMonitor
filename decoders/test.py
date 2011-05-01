#!/usr/bin/env python

import sys, os
if os.path.dirname(os.path.abspath(__file__)) in sys.path:
	sys.path.remove(os.path.dirname(os.path.abspath(__file__)))
if os.path.dirname(os.path.dirname(os.path.abspath(__file__))) not in sys.path:
	sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import decoders, events

def onAllMessages(event, data):
	sys.stdout.write('%f : ' % data[0])
	sys.stdout.write('%s - ' % event)
	print(data[1])

events.register_all(decoders.IrisDecoder, onAllMessages)

sys.stdout.write('Available decoders are :\n')
i = 0
declist = decoders.get_list()
for d in declist:
	sys.stdout.write('  %3d    %s\n' % (i, d))
	i += 1
try:
	if len(declist) == 0:
		sys.stderr.write('No channel available.\n')
	if len(declist) == 1:
		a = 0
	else:
		sys.stdout.write('Which one would be tested ? ')
		sys.stdout.flush()
		a = int(sys.stdin.readline())
	sys.stdout.write('Test of `%s`\n' % declist[a])
	theclass = decoders.get_class(declist[a])
	decoder = theclass()
except ValueError:
	sys.exit('Invalid number.\n')
except IndexError:
	sys.exit('Unknowed entry.\n')
except KeyboardInterrupt:
	sys.exit('Interrupted test.\n')

sys.stdout.write('The decoder has to be tested in conjunction with a channel.\n')

from channels import test
