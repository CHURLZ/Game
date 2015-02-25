
class action:
	MOVE_TO = 0
	MOVE_OBJECT = 1
	actionType = 0

	owner = None
	interactFrom = None
	interactTo = None
	interactionObject = None
	isDone = False

	def __init__(self, typeOfTask, intFrom, intTo, obj):
		self.actionType = typeOfTask
		self.interactFrom = intFrom
		self.interactTo = intTo
		self.interactionObject = obj