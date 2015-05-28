
class action:
	MOVE_TO = 0
	MOVE_OBJECT = 1
	PICK_UP_OBJECT = 2
	DROP_OBJECT = 3
	actionType = 0

	names=["moving to", "moving stuff!", "picking stuff up!", "leaving this here."]

	owner = None
	interactFrom = None
	interactTo = None
	interactionObject = None
	interactZone = None
	isDone = False

	def __init__(self, typeOfTask, intFrom, intTo, obj, zone):
		self.actionType = typeOfTask
		self.interactFrom = intFrom
		self.interactTo = intTo
		self.interactionObject = obj
		self.interactZone = zone