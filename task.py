import Queue
from action import *

class Task:
	MOVE_TO = 0
	MOVE_OBJECT = 1
	PICK_UP_OBJECT = 2
	DROP_OBJECT = 3
	taskType = 0

	owner = None
	interactFrom = None
	interactTo = None
	interactionObject = None

	def __init__(self, typeOfTask, intFrom, intTo, obj, zone):
		self.actions = Queue.Queue()
		self.taskType = typeOfTask
		self.interactFrom = intFrom
		self.interactTo = intTo
		self.interactionObject = obj

		if typeOfTask == self.MOVE_TO:
			self.actions.put(action(self.MOVE_TO, None, intTo, obj, zone))
		elif typeOfTask == self.MOVE_OBJECT:
			self.actions.put(action(self.MOVE_TO, None, intFrom, obj, zone))
			self.actions.put(action(self.PICK_UP_OBJECT, None, None, obj, None))
			self.actions.put(action(self.MOVE_OBJECT, None, intTo, obj, None))
			self.actions.put(action(self.DROP_OBJECT, None, None, obj, None))
		elif typeOfTask == self.PICK_UP_OBJECT:
			self.actions.put(action(self.MOVE_TO, None, intFrom, obj, None))
			self.actions.put(action(self.PICK_UP_OBJECT, None, None, obj, None))
		elif typeOfTask == self.DROP_OBJECT:
			self.actions.put(action(self.DROP_OBJECT, None, None, obj, zone))

	def takeAction(self):
		if not self.actions.empty():
			return self.actions.get()

	def isDone(self):
		return self.actions.empty()
