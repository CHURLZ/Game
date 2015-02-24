import pygame, Queue
from task import *
class taskManager:
	
	tasks = Queue.Queue()

	@staticmethod
	def addTask(taskType, taskFrom, taskTo, taskObj):
		taskManager.tasks.put(task(taskType, taskFrom, taskTo, taskObj))
	
	@staticmethod
	def takeTask():
		if not isEmpty():
			return taskManager.tasks.pop()	
	@staticmethod
	def isEmpty():
		return len(taskManager.tasks) == 0

