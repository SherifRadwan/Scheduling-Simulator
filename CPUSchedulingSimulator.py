#!/usr/bin/env python

from scheduler.job import *
from scheduler.fcfs import *
from scheduler.sjf import *
from scheduler.srjf import *
from scheduler.priority import *
from scheduler.preemptive_priority import *
from scheduler.round_robin import *

from PyQt4 import QtCore, QtGui
from random import randint
import copy
import time

class JobWidget(QtGui.QLabel):

	# todo add colors
	def __init__(self, text=''):
		QtGui.QLabel.__init__(self, None)
		self.setText(text)
		self.setFrameShape(QtGui.QFrame.Box)
		self.setWordWrap(True)
		self.setIndent(0)
		self.setFont(QtGui.QFont("Times", 20))#, QtGui.QFont.Bold))
		#self.setScaledContents(True)

	#def __copy__(self):
	#	 #http://stackoverflow.com/questions/1500718/what-is-the-right-way-to-override-the-copy-deepcopy-operations-on-an-object-in-p
  	#	newone = type(self)()
  	#	newone.__dict__.update(self.__dict__)
  	#	return newone

# need to be improved or changed
# TODO: reimplement this in QGraphics scene and view
class JobListWidget(QtGui.QScrollArea):
	def __init__(self, title='', allowDuplicates = False, spacing = 5):
		QtGui.QLabel.__init__(self, None)
		self.widget = QtGui.QWidget()
		self.titleLbl = QtGui.QLabel(title)
		self.hbox = QtGui.QHBoxLayout()
		self.hbox.setSpacing(spacing)
		self.vbox = QtGui.QVBoxLayout()
		self.vbox.addWidget(self.titleLbl)
		self.vbox.addLayout(self.hbox)

		self.widget.setLayout(self.vbox)
		self.allowDuplicates = allowDuplicates
		self.widgets = []
		self.hbox.addStretch() # last one
		self.setWidgetResizable(True)
		self.setWidget(self.widget)

	def addWidget(self, widget, sub_text=None):
		if not self.allowDuplicates and self.hbox.indexOf(widget) != -1:
			return

		if self.allowDuplicates:
			#widget = copy.copy(widget)
			#widget = copy.deepcopy(widget)
			widget = JobWidget(widget.text())

		if sub_text:
			widget.setText(widget.text() + '<sub>%s</sub>' % sub_text)

		self.widgets.append(widget)

		self.hbox.insertWidget(self.hbox.count() - 1, widget)
		widget.show()

	def removeWidget(self, widget):
		#widget.clearLayout()
		if self.hbox.indexOf(widget) != -1:
			self.hbox.removeWidget(widget)

	def clear(self):
		# delete error causes some error if called agian
		# figure it out
		for widget in self.widgets:
			try:
				widget.deleteLater()
			except:
				continue

class SchedulerWidget(QtGui.QWidget):

	def __init__(self):
		QtGui.QWidget.__init__(self, None)
		self.resize(700, 500)
		self.setWindowTitle('CPU Scheduling Simulator')
		self.sch = None
		self.jobs = []
		self.init_ui()

	def init_ui(self):
		self.timer = QtCore.QTimer()
		self.timer.setInterval(1000) # one second
		self.timer.timeout.connect(self.tick)

		self.numLbl = QtGui.QLabel('No. of jobs: ')
		self.jobs_no = QtGui.QSpinBox()
		self.jobs_no.setValue(5)
		self.jobs_no.valueChanged[int].connect(lambda v: self.generateJobs())
		self.generateBtn = QtGui.QPushButton('&Generate')
		self.startBtn = QtGui.QPushButton('&Start')
		self.startBtn.setEnabled(False)
		self.stopBtn = QtGui.QPushButton('&Stop')
		self.stopBtn.setEnabled(False)
		self.pauseBtn = QtGui.QPushButton('&Pause')
		self.pauseBtn.clicked.connect(self.pauseSimu)
		self.resumeBtn = QtGui.QPushButton('&Resume')
		self.resumeBtn.clicked.connect(self.resumeSimu)
		self.pauseBtn.setEnabled(False)
		self.resumeBtn.setVisible(False)
		self.generateBtn.clicked.connect(self.generateJobs)
		self.startBtn.clicked.connect(self.startSimu)
		self.stopBtn.clicked.connect(self.stopSimu)
		self.speedLbl = QtGui.QLabel('Speed: ')
		self.speedSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
		self.speedSlider.setMinimum(0)
		self.speedSlider.setMaximum(10)
		self.speedSlider.setValue(1)
		self.speedSlider.valueChanged[int].connect(lambda v: self.timer.setInterval(v*1000))
		self.timeLbl = QtGui.QLabel('Time: ')
		self.controlLayout = QtGui.QHBoxLayout()
		self.controlLayout.addWidget(self.numLbl)
		self.controlLayout.addWidget(self.jobs_no)
		self.controlLayout.addWidget(self.generateBtn)
		self.controlLayout.addWidget(self.startBtn)
		self.controlLayout.addWidget(self.stopBtn)
		self.controlLayout.addWidget(self.pauseBtn)
		self.controlLayout.addWidget(self.resumeBtn)
		self.controlLayout.addWidget(self.speedLbl)
		self.controlLayout.addWidget(self.speedSlider)		
		self.controlLayout.addWidget(self.timeLbl)

		self.algorithms = [FCFS, SJF, SRJF, Priority, PreemptivePriority, RoundRobin]
		self.algoLabel = QtGui.QLabel('Algorithm: ')
		self.comoboAlgo = QtGui.QComboBox()
		self.comoboAlgo.activated[int].connect(self.algoChoosed)
		self.timeSliceLabel = QtGui.QLabel('Time Slice: ')
		self.timeSliceSpin = QtGui.QSpinBox()
		self.timeSliceSpin.setMinimum(1)
		self.timeSliceSpin.setValue(1)
		self.timeSliceLabel.setVisible(False)
		self.timeSliceSpin.setVisible(False)
		self.comoboAlgo.setCurrentIndex(0)
		self.algoChoosed(0)
		self.comoboAlgo.addItems(['FCFS', 'SJF', 'SRJF', 'Priority', 'Preemptive Priority', 'RoundRobin'])
		self.algoLayout = QtGui.QHBoxLayout()
		self.algoLayout.addWidget(self.algoLabel)
		self.algoLayout.addWidget(self.comoboAlgo)
		self.algoLayout.addWidget(self.timeSliceLabel)
		self.algoLayout.addWidget(self.timeSliceSpin)
		self.algoLayout.addStretch()
		self.aboutBtn = QtGui.QPushButton('&About')
		self.aboutBtn.clicked.connect(self.aboutMsg)
		self.algoLayout.addWidget(self.aboutBtn)
		# control algo layout
		self.calgoLayout = QtGui.QVBoxLayout()
		self.calgoLayout.addLayout(self.controlLayout)
		self.calgoLayout.addLayout(self.algoLayout)
		self.calgoLayout.addStretch()

		self.jobsTable = QtGui.QTableWidget(0, 3)
		self.generateJobs()
		# calgoLayout and table
		self.splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
		self.calgoWidget = QtGui.QWidget()
		self.calgoWidget.setLayout(self.calgoLayout)
		self.splitter.addWidget(self.calgoWidget)
		self.splitter.addWidget(self.jobsTable)

		self.new_jobs = JobListWidget('New')
		self.ready_jobs = JobListWidget('Ready')
		self.running_jobs = JobListWidget('Running', True, 0)
		self.terminated_jobs = JobListWidget('Terminated')

		self.avgTurnaround = QtGui.QLabel('Average Turnaround time: ')
		self.avgWaiting = QtGui.QLabel('Average Waiting time: ')
		self.cpuUtilization = QtGui.QLabel('CPU Utilization: ')

		self.mainLayout = QtGui.QVBoxLayout()
		self.mainLayout.addWidget(self.splitter)
		self.mainLayout.addWidget(self.new_jobs)
		self.mainLayout.addWidget(self.ready_jobs)
		self.mainLayout.addWidget(self.running_jobs)
		self.mainLayout.addWidget(self.terminated_jobs)
		self.mainLayout.addStretch()
		self.mainLayout.addWidget(self.avgTurnaround)
		self.mainLayout.addWidget(self.avgWaiting)
		self.mainLayout.addWidget(self.cpuUtilization)

		self.setLayout(self.mainLayout)

	def tick(self):
		if self.sch:
			# to get the ready ones
			#self.sch.get_ready_jobs(self.sch.current_time)
			self.report_scheduler(self.sch)
			#time.sleep(0.3)
			self.timeLbl.setText('Time: %d' % self.sch.current_time)
			if self.sch.isFinished():
				self.stopSimu()
				self.avgTurnaround.setText('Average Turnaround time:  %f' % self.sch.avg_turnaround_time())
				self.avgWaiting.setText('Average Waiting time:  %f' % self.sch.avg_waiting_time())
				self.cpuUtilization.setText('CPU Utilization: %f' % (self.sch.cpu_util() * 100.0) + '%')
			else:
				self.sch.tick()

	def report_scheduler(self, sch):
		for job in sch.ready:
			self.add_to_ready(job.widget)

		if sch.current_job:
			self.add_to_running(sch.current_job.widget)

		for job in sch.terminated:
			self.add_to_terminated(job.widget)

		#if self.sch.isIdle():
		#	self.add_to_running(JobWidget('  '))

	def add_to_new(self, widget):
		###
		self.new_jobs.addWidget(widget)

	def add_to_ready(self, widget):
		self.new_jobs.removeWidget(widget)
		self.ready_jobs.addWidget(widget)

	def add_to_running(self, widget):
		#widget.setText(widget.text() + )
		self.ready_jobs.removeWidget(widget)
		self.running_jobs.addWidget(widget, self.sch.current_time)

	def add_to_terminated(self, widget):
		self.terminated_jobs.addWidget(widget)

	def job_status_changed(self, job, new_status):
		if 	 new_status == Status.Ready:
			self.add_to_ready(job.widget)
		elif new_status == Status.Running:
			self.add_to_running(job.widget)
		elif new_status == Status.Terminated:
			self.add_to_terminated(job.widget)

	def algoChoosed(self, index):
		self.algo = self.algorithms[index]

		if self.algo == RoundRobin:
			self.timeSliceLabel.setVisible(True)
			self.timeSliceSpin.setVisible(True)
		else:
			self.timeSliceLabel.setVisible(False)
			self.timeSliceSpin.setVisible(False)

	def generateJobs(self):
		self.startBtn.setEnabled(True)

		n = self.jobs_no.value()

		if n > 0:
			self.jobsTable.clear()
			self.jobsTable.setRowCount(n)

			for r in range(0, self.jobsTable.rowCount()):
				self.jobsTable.setItem(r, 0, QtGui.QTableWidgetItem(str(randint(0, n))))
				self.jobsTable.setItem(r, 1, QtGui.QTableWidgetItem(str(randint(1, n))))
				self.jobsTable.setItem(r, 2, QtGui.QTableWidgetItem(str(randint(0, n))))
			
			self.jobsTable.setVerticalHeaderLabels(['P%d'%p for p in range(1, n+1)])
			self.jobsTable.setHorizontalHeaderLabels(['Arrival Time', 'Bursts', 'Priority'])


	def startSimu(self):
		self.new_jobs.clear()
		self.ready_jobs.clear()
		self.running_jobs.clear()
		self.terminated_jobs.clear()
		self.avgTurnaround.setText('Average Turnaround time: ')
		self.avgWaiting.setText('Average Waiting time: ')
		self.jobs = []

		for r in range(0, self.jobsTable.rowCount()):
			arrival_time = int(self.jobsTable.item(r, 0).text())
			brusts = int(self.jobsTable.item(r, 1).text())
			priority = int(self.jobsTable.item(r, 2).text())
			job = Job(bursts=brusts, arrival_time=arrival_time, priority=priority, job_id=r+1)
			widget = JobWidget('P%d' % job.job_id)
			job.widget = widget
			self.jobs.append(job)
			self.add_to_new(job.widget)

		#self.sch = FCFS(self.jobs)
		if self.algo == RoundRobin:
			self.sch = RoundRobin(self.timeSliceSpin.value(), self.jobs)
		else:
			self.sch = self.algo(self.jobs)

		self.stopBtn.setEnabled(True)
		self.pauseBtn.setEnabled(True)
		self.startBtn.setEnabled(False)
		self.timer.start()

	def stopSimu(self):
		self.timer.stop()
		self.stopBtn.setEnabled(False)
		self.pauseBtn.setEnabled(False)
		self.startBtn.setEnabled(True)
		self.resumeBtn.setVisible(False)
		self.pauseBtn.setVisible(True)

	def pauseSimu(self):
		self.timer.stop()
		self.pauseBtn.setVisible(False)
		self.resumeBtn.setVisible(True)

	def resumeSimu(self):
		self.timer.start()
		self.pauseBtn.setVisible(True)
		self.resumeBtn.setVisible(False)
	
	def aboutMsg(self):
		QtGui.QMessageBox.about(self, 'About', 'CPU Scheduling Simulator<br>Operating Systems Project<br>By: Abdelrahman Ghanem')

if __name__ == '__main__':
	import sys

	app = QtGui.QApplication(sys.argv)
  	en_eg= QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Egypt)
  	QtCore.QLocale.setDefault(en_eg)
	mwin = SchedulerWidget()
	mwin.show()
	sys.exit(app.exec_())
