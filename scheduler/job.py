# job is shorter than process, also jobs proccesses :D

__all__ = ['Status', 'Job']

""" 
	represent the process status,
	with string values
"""
class Status(object):
	New, Ready, Waiting, Running, Terminated = range(0, 5)
	Strings = ['New', 'Ready', 'Waiting', 'Running', 'Terminated']


class Job(object):

	def __init__(self, bursts, arrival_time = 0, priority = 0, job_id = None):
		""" 
			init the process with required information 
			every algorihtm would use some of this attributes
		"""
		self.arrival_time = arrival_time
		self.priority = priority
		self.bursts = bursts
		# this will remain for later calcualtions
		# or we can check if the process has finished
		# by cheching current time - start time if it equals
		# to bursts
		self.cpu_bursts = bursts
		self.__status = Status.New
		self.compare_attr = 'priority'
		self.start_time = 0
		self.finish_time = 0

		# optional job identifier
		self.job_id = job_id
		self.widget = None # graphic representation
	
	#arrival_time = properity(fset, fget...)
	#brusts = ...
	def __get_status(self):
		return self.__status

	def __set_status(self, new_status):
		self.__status = new_status

	status = property(__get_status, __set_status)
	
	def str_status(self):
		return Status.Strings[self.__status]

	def turnaround(self):
		return self.finish_time - self.arrival_time

	def waiting(self):
		return self.turnaround() - self.cpu_bursts

	def response(self):
		return self.start_time - self.arrival_time

	def __isub__(self, other):
		""" 
			when using -= it would sub rhs from self.brusts
			and check for the job termination
		"""

		if isinstance(other, int):
			self.bursts -= other

			if self.bursts == 0:
				self.status = Status.Terminated

		return self

	def __cmp__(self, other):
		"""
			this is called when comparing self with another object
			>, <, >= ....etc
			this will help in using the job type
			in iteratables then apply max, min...etc on them
		"""

		if isinstance(other, Job):

			a = getattr(self, self.compare_attr)
			b = getattr(other, self.compare_attr)
		
			if a > b:
				return 1
			elif a < b:
				return -1
			else:
				# all attributes are the same?
				if self.__dict__ == other.__dict__:
					return 0
				else:
					return -1 # or 1 or anything unknown!

	#def __str__(self):
	#	return ''.join(['%s %s\n' % (k, v) for k, v in self.__dict__.items()])

	def __repr__(self):
		return '<job object at %d> <%s>' % (id(self), self.str_status())

if __name__ == '__main__':
	# some tests

	p1 = Job(5, priority = 2)
	p2 = Job(5, priority = 3)
	p3 = Job(5, priority = 3)

	p1 -= 1
	print p1.bursts
	
	print p1 == p2

	j1 =  min([p1, p2, p3])
	j2 =  max([p1, p2, p3])
	print j1
	print j2
