class stack(list):
	def __init__(self, iteratable = None): 
		#check for iteratable, try..except
		if iteratable:
			list.__init__(self, iteratable)
		else:
			list.__init__(self)

	def push(self, item):
		self.append(item)





if __name__ == '__main__':
	s = stack()
	for i in range(1, 11):
		s.push(i)

	print 'stack length: %d' % len(s)

	for i in range(1, 11):
		print s.pop()

	st = stack([5,6,7])
	print st