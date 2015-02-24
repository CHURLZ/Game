class God():
	cameraX = 100
	cameraY = 0
	
	CAMERA_SPEED_NORMAL = 5
	CAMERA_SPEED_FAST = 15
	cameraSpeed = CAMERA_SPEED_NORMAL
	cameraSpeedX = 0
	cameraSpeedY = 0

	key_w = False
	key_s = False
	key_a = False
	key_d = False
	key_LSHIFT = False

	def __init__(self):
		print "allahu akbar"

	def update(self):
		if self.key_LSHIFT:
			self.CAMERA_SPEED = self.CAMERA_SPEED_FAST
		else:
			self.CAMERA_SPEED = self.CAMERA_SPEED_NORMAL

		if self.key_w:
			self.cameraSpeedY = self.CAMERA_SPEED
		elif self.key_s:
			self.cameraSpeedY = -self.CAMERA_SPEED
		else:
			self.cameraSpeedY = 0

		if self.key_a:
			self.cameraSpeedX = self.CAMERA_SPEED
		elif self.key_d:
			self.cameraSpeedX = -self.CAMERA_SPEED
		else:
			self.cameraSpeedX = 0


		self.cameraX += self.cameraSpeedX
		self.cameraY += self.cameraSpeedY

	@staticmethod
	def getCamera():
		return {CAMERA_X, CAMERA_Y}

