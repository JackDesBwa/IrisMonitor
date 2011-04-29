#!/usr/bin/env python
import sys, channels, decoders, events

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
sys.stdout.write('Available channels are :\n')
i = 0
chanlist = channels.get_list()
for c in chanlist:
	sys.stdout.write('  %3d    %s\n' % (i, c))
	i += 1

try:
	if len(chanlist) == 0:
		sys.stderr.write('No channel available.\n')
	if len(chanlist) == 1:
		a = 0
	else:
		sys.stdout.write('Which one would be used ? ')
		sys.stdout.flush()
		a = int(sys.stdin.readline())
	sys.stdout.write('Test with `%s`\n' % chanlist[a])
	theclass = channels.get_class(chanlist[a])
	chan = theclass()
except ValueError:
	sys.stderr.write('Invalid number.\n')
except IndexError:
	sys.stderr.write('Unknowed entry.\n')
except KeyboardInterrupt:
	sys.exit('Interrupted test.\n')

try:
	chan.run()
except KeyboardInterrupt:
	sys.stdout.write('End of test.\n')
