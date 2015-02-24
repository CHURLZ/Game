class task:
	MOVE_TO = 0
	MOVE_OBJECT = 1
	task = 0

	owner = None
	interactFrom = None
	interactTo = None
	interactionObject = None
	isDone = False

	def __init__(self, typeOfTask, own, interactFrom=None, interactTo=None, obj=None):
		task = typeOfTask
		owner = own
		interactTo = interactTo
		interactFrom = interactFrom