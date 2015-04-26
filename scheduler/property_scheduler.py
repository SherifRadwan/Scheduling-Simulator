from scheduler.algorithm import *

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
class PropertyScheduler(SchedulingAlgorithm):
	""" schedule given jobs according to certain property """

	def __init__(self, attr, jobs = []):
		""" set choosed attribute/property to schedule on """
		SchedulingAlgorithm.__init__(self, attr, jobs)

	def get_a_ready_job(self):
		""" get a ready job according to property self.attr """
		return self.select_job(self.ready)

	def preempt(self):
		"""
			preemptive schduling
		"""
		if self.current_job:
			# get a job and compare it with the current one
			next_job = self.select_job(self.ready)

			# got one?
			if next_job:
				# the prev job selected by comparison
				prev_job = self.select_func([self.current_job,
									     	 next_job])

				# the prev job is the same as current one
				if prev_job == self.current_job:
					# things still as it is, prev is next
					self.context_switch(next_job, self.current_job)
				else:
					# assign next to be the next job
					self.context_switch(self.current_job, next_job)


	def tick(self):
		super(PropertyScheduler, self).tick()

		# time now is +1
		# preempt if it is possible
		if self.preemptive:
			self.preempt()


if __name__ == '__main__':
	# import relative util stack and queue
	# jobs = [Job(10), Job(5), Job(7), Job(2), Job(3)]
	# sch = PropertyScheduler('priority', jobs)
	# sch.select_func = min
	
	# for i in range(0, 15):
	# 	sch.tick()
	# 	print len(sch.ready), sch.ready
	# 	print sch.current_job
	# 	print "-----------------------"

	jobs1 = [Job(10, arrival_time=5, priority=2),
			Job(2, arrival_time=15, priority=0),
			Job(4, arrival_time=7, priority=5),
			Job(7, arrival_time=3, priority=2),
			Job(7, arrival_time=2, priority=1),
			Job(2, arrival_time=1, priority=0),
			Job(3, arrival_time=0, priority=3)]
	

	jobs2 = [Job(100, arrival_time=0),
			Job(10, arrival_time=10, priority = 1),
			Job(10, arrival_time=10, priority = 3)]
	


	#sch = PropertyScheduler('priority', jobs)
	sch = PropertyScheduler('bursts', jobs2)
	sch.select_func = min
	sch.preemptive = True

	while not sch.isFinished():
		sch.tick()
		print "Time:", sch.current_time
		j = sch.current_job
		if j: print j.cpu_bursts, j.bursts, j.priority
		#if j: print j.arrival_time, j.priority, j.bursts

	print [job.finish_time for job in sch.terminated]
	print sch.avg_turnaround_time()