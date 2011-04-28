import sys, channels, events

onReceive_col = 0
def onReceive(byte):
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

try:
	sys.stdout.write('Which one would be tested ? ')
	a = int(sys.stdin.readline())
	sys.stdout.write('Test of `%s`\n' % chanlist[a])
	theclass = channels.get_class(chanlist[a])
	chan = theclass()
	chan.run()
except ValueError:
	sys.stdout.write('Invalid number.\n')
except IndexError:
	sys.stdout.write('Unknowed entry.\n')
except KeyboardInterrupt:
	sys.stdout.write('End of test.\n')
