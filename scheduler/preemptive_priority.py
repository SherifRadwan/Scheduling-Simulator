from scheduler.property_scheduler import PropertyScheduler

class PreemptivePriority(PropertyScheduler):

	def __init__(self, jobs = []):
		PropertyScheduler.__init__(self, 'priority', jobs)
		self.select_func = min
		self.preemptive = True

