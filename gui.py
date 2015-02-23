import pygame, images

BUTTON_WIDTH = 30
BUTTON_HEIGHT = 30

class GUIBaseClass(pygame.sprite.Sprite):
	allSprites = pygame.sprite.OrderedUpdates()

	def __init__(self, x, y, width, height, image):
		pygame.sprite.Sprite.__init__(self)

		GUIBaseClass.allSprites.add(self)

		self.image = image.convert_alpha()
		self.image.set_alpha(100)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = width
		self.height = height
		self.walkX = x + (width / 2)
		self.walkY = y + height 
		self.centerX = self.walkX
		self.centerY = self.rect.y + (height / 2)

class ActionPanel(GUIBaseClass):
	buttons = pygame.sprite.Group()
	def __init__(self, x, y, width, height, image):
		GUIBaseClass.__init__(self, x, y, width, height, image)

		

		self.buttons.add(ZoningButton(self.rect.x + 10, self.rect.y + 20, BUTTON_WIDTH, BUTTON_HEIGHT, images.zoneButton))
		self.buttons.add(WallingButton(self.rect.x + 10, self.rect.y + BUTTON_HEIGHT + 40, BUTTON_WIDTH, BUTTON_HEIGHT, images.wallButton))

class ActionButton(ActionPanel):
	def __init__(self, x, y, width, height, image):
		GUIBaseClass.__init__(self, x, y, width, height, image)

		ActionPanel.buttons.add(self)
		
	def onClick(self):
		return

class WallingButton(ActionButton):
	def __init__(self, x, y, width, height, image):
		ActionButton.__init__(self, x, y, width, height, image)

	def onClick(self, builder):
		builder.state = builder.WALL
		print "WALLING"

class ZoningButton(ActionButton):
	def __init__(self, x, y, width, height, image):
		ActionButton.__init__(self, x, y, width, height, image)

	def onClick(self, builder):
		builder.state = builder.ZONE
		print "ZONING"
