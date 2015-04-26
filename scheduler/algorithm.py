# will use an ordinary list and sort it 
# with any attr
#TODO: options for
	# preemptive or not
	# time slice or not
	# or don't put every thing in one place ??
	# just make a common things between this and its subclasses
	# like ready queue, waiting queue, running...etc

# TODO: add a feature to set a certain job/process to waiting status
# should be priority scheduler

from scheduler.job import *

class SchedulingAlgorithm(object):

	def __init__(self, attr, jobs = []):
		self.total_jobs = len(jobs)
		self.total_time = sum([job.cpu_bursts for job in jobs])

		self.current_time = 0
		self.current_job = None
		
		# in case of switching
		self.next_job = None 

		# set comparing property
		self.attr = attr
		for job in jobs:
			job.compare_attr = attr
		self.jobs = jobs
	
		self.ready = [] #queue(), set as you want
		self.context_stack = [] # stack()
		self.waiting = [] # queue(), in case of i/o request
		self.terminated = []

		self.__select_func = min
		self.preemptive = False

		self.idle_time = 0

	def __get_sel_func(self):
		return self.__select_func

	def __set_sel_func(self, func):
		# to get the first minimum if the two are the same
		# l = [a, b]
		# if a = b, to get a not b, just reverse the list
		if func == min:
			self.jobs = list(reversed(self.jobs))
		self.__select_func = func

	select_func = property(__get_sel_func, __set_sel_func)


	def get_ready_jobs(self, time):
		""" 
		   get the jobs ready at t = time
		   then put them in ready jobs list
		 """
		ready_jobs = []

		# get ready ones
		for job in self.jobs:
			if job.arrival_time <= time:
				job.status = Status.Ready
				self.ready.append(job)
				ready_jobs.append(job)

		# remove them from jobs list
		for job in ready_jobs:
			self.jobs.remove(job)

	def select_job(self, jobs = []):
		""" 
		    select a job from the a given jobs,
		    according to select function (max, min, ...etc)
		    and comapre attribute
		"""

		if jobs:
			job = self.__select_func(jobs)
			if job.arrival_time <= self.current_time:
				jobs.remove(job)
				return job

		return None # just to see it

	def get_a_ready_job(self):
		""" 
			reimplement this in sub class,
			this shows how to get a ready a job from ready list
		"""
		raise NotImplementedError

	def dispatch_next(self):
		""" 
			get a ready job and assign it to execution
		"""

		if self.next_job:
			self.current_job = self.next_job
			self.next_job = None

		if not self.current_job or self.current_job.status == Status.Terminated:
			# get one
			self.current_job = self.get_a_ready_job()


	def process(self):
		"""
			process current assigned job
		"""

		# dispatch a ready job
		self.dispatch_next()

		# no ready job, return
		if not self.current_job: return

		# ok, got a job then give it some clocks!
		self.current_job -= 1

		# completed?
		if self.current_job.status == Status.Terminated:
			self.current_job.finish_time = self.current_time + 1
			self.terminated.append(self.current_job)
		else:
			self.current_job.status = Status.Running

	def tick(self):
		# clk, clk, clk
		if self.isFinished():
			return

		# get the rady jobs at current time
		self.get_ready_jobs(self.current_time)

		# process them
		self.process()

		# time++
		self.current_time += 1
		
		# get the rady jobs again
		# wil need this to accurately
		# report the ready jobs at a certain time
		# and access them via self.ready
		# i.e. see property_scheduler or round_robin
		self.get_ready_jobs(self.current_time)

		# see if it's idle or not to get overall utilization
		if self.isIdle(): self.idle_time += 1

	def isIdle(self):
		if self.current_job: return False
		return True

	def isFinished(self):
		# sometimes it doesn't work if one job arrived at 0 time
    	# // this will not be right if the first job arrives at t >= 0
		#return self.total_time == self.current_time
		return len(self.terminated) == self.total_jobs

	def context_switch(self, prev, next):
		# http://lxr.free-electrons.com/source/kernel/sched/core.c#L2234
		""" switch the prev job with the given next job """
		# it should switch with the context stack
		# but here we will dispatch next to cpu
		# and put prev back to the ready list
		if prev.status != Status.Terminated:
			self.ready.append(prev)
			prev.status = Status.Ready

		if next.status != Status.Terminated:
			self.next_job = next
			next.status = Status.Running

	def avg_time(self, fn):
		""" just get average from the function name """
		times = [getattr(job, fn)() for job in self.terminated]
		return sum(times) / float(len(times))

	def avg_turnaround_time(self):
		return self.avg_time('turnaround')

	def avg_waiting_time(self):
		return self.avg_time('waiting')

	def avg_response_time(self):
		return self.avg_time('response')


	def cpu_util(self):
		return float(self.current_time - self.idle_time) / self.current_time


if __name__ == '__main__':
	pass