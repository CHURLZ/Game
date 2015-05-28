import pygame, Queue
from task import *
class TaskManager:
	
	tasks = Queue.Queue()

	@staticmethod
	def addTask(taskType, taskFrom, taskTo, taskObj, taskZone):
		newTask = Task(taskType, taskFrom, taskTo, taskObj, taskZone)
		TaskManager.tasks.put(newTask)
	
	@staticmethod
	def takeTask():
		if not TaskManager.isEmpty():	
			return TaskManager.tasks.get(False)

	@staticmethod
	def isEmpty():
		return TaskManager.tasks.empty()

