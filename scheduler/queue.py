from collections import deque

class queue(deque):

	def __init__(self, iteratable = None):
		if iteratable:
			deque.__init__(self, iteratable)
		else:
			deque.__init__(self)


	def enqueue(self, item):
		self.append(item)


	def dequeue(self):
		if self:
			return self.popleft()


if __name__ == '__main__':
	q = queue()
	for i in range(1, 11):
		q.enqueue(i)

	print 'queue length: %d' % len(q)

	for i in range(1, 11):
		print q.dequeue()

	qu = queue([5,6,7])
	print qu
