import pygame, Queue
from task import *
class taskManager:
	
	tasks = Queue.Queue()

	@staticmethod
	def addTask(taskType, taskFrom, taskTo, taskObj):
		newTask = task(taskType, taskFrom, taskTo, taskObj)
		taskManager.tasks.put(newTask)

	@staticmethod
	def takeTask():
		if not taskManager.isEmpty():	
			return taskManager.tasks.get(False)

	@staticmethod
	def isEmpty():
		return taskManager.tasks.empty()

