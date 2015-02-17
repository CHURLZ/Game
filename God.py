class God():
	CAMERA_X = 0
	CAMERA_Y = 0
	
	CAMERA_SPEED_NORMAL = 5
	CAMERA_SPEED_FAST = 10
	CAMERA_SPEED = CAMERA_SPEED_NORMAL

	key_w = False
	key_s = False
	key_a = False
	key_d = False
	key_LSHIFT = False

	def __init__(self):
		print "allahu akbar"

	def update(self):
		if self.key_w:
			self.CAMERA_Y = self.CAMERA_SPEED
		elif self.key_s:
			self.CAMERA_Y = -self.CAMERA_SPEED
		else:
			self.CAMERA_Y = 0

		if self.key_a:
			self.CAMERA_X = self.CAMERA_SPEED
		elif self.key_d:
			self.CAMERA_X = -self.CAMERA_SPEED
		else:
			self.CAMERA_X = 0

		if self.key_LSHIFT:
			self.CAMERA_SPEED = self.CAMERA_SPEED_FAST
		else:
			self.CAMERA_SPEED = self.CAMERA_SPEED_NORMAL

