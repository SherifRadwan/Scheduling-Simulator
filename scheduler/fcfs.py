from scheduler.property_scheduler import PropertyScheduler

""" First-Come-First-Serverd scheduling """
class FCFS(PropertyScheduler):

	def __init__(self, jobs = []):
		""" schedule on arrival time """
		PropertyScheduler.__init__(self, 'arrival_time', jobs)
		self.select_func = min

if __name__ == '__main__':
	jobs = [Job(2, arrival_time=1),
			Job(2, arrival_time=2),
			Job(1, arrival_time=5),
			Job(3, arrival_time=3),
			Job(4, arrival_time=4)]

	sch = FCFS(jobs)

	# note, jobs are reversed in case of min function

	while not sch.isFinished():
		sch.tick()
		print "Time: ", sch.current_time
		j = sch.current_job
		if j:
			print j.cpu_bursts, j.bursts
		#print sch.ready
		#print sch.terminated
	
	print [job.finish_time for job in sch.terminated]