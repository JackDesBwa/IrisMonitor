import viewers, decoders, channels

print 'Iris monitor first main'
print 'Available viewers are :'
for v in viewers.get_list():
	print '\t%s' % v
print 'Available decoders are :'
for d in decoders.get_list():
	print '\t%s' % d
print 'Available channels are :'
for c in channels.get_list():
	print '\t%s' % c
