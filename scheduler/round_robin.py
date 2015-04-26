from scheduler.queue import *
from scheduler.algorithm import SchedulingAlgorithm

class RoundRobin(SchedulingAlgorithm):

	def __init__(self, time_slice = 1, jobs = []):
		SchedulingAlgorithm.__init__(self, 'arrival_time', jobs)
		self.ready = queue()
		self.time_slice = time_slice
		self.slice_counter = self.time_slice

	def get_a_ready_job(self):
		return self.ready.dequeue()

	def tick(self):
		super(RoundRobin, self).tick()

		if self.current_job:
			self.slice_counter -= 1

		if self.slice_counter == 0:
			self.slice_counter = self.time_slice
			if self.ready:
				next_job = self.get_a_ready_job()
				if next_job:
					self.context_switch(self.current_job, next_job)


if __name__ == '__main__':
	jobs = [Job(5, arrival_time=0),
			Job(5, arrival_time=0),
			Job(4, arrival_time=0)]
	
	sch = RoundRobin(3, jobs)

	while not sch.isFinished():
		sch.tick()
		print "Time:", sch.current_time
		j = sch.current_job
		if j: print j, j.cpu_bursts, j.bursts
		#if j: print j.arrival_time, j.priority, j.bursts

	print [job.finish_time for job in sch.terminated]
	print sch.avg_turnaround_time()
	print sch.avg_response_time()