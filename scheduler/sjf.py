from scheduler.property_scheduler import PropertyScheduler

""" Shortes-Job-First """
class SJF(PropertyScheduler):

	def __init__(self, jobs = []):
		PropertyScheduler.__init__(self, 'bursts', jobs)
		self.select_func = min


if __name__ == '__main__':
	jobs = [Job(10, arrival_time=0, priority=1),
			Job(3, arrival_time=0, priority=2),
			Job(3, arrival_time=0, priority=1),
			Job(5, arrival_time=0, priority=1)]

	sch = SJF(jobs)

	# note, jobs are reversed in case of min function
	
	while not sch.isFinished():
		sch.tick()
		print "Time: ", sch.current_time
		j = sch.current_job
		if j:
			print j.cpu_bursts, j.bursts, j.priority

	print [job.finish_time for job in sch.terminated]
