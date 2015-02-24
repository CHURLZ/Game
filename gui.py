import pygame, images

BUTTON_WIDTH = 30
BUTTON_HEIGHT = 30

class GUIBaseClass(pygame.sprite.Sprite):
	allSprites = pygame.sprite.OrderedUpdates()

	def __init__(self, x, y, width, height, image, alpha):
		pygame.sprite.Sprite.__init__(self)
		GUIBaseClass.allSprites.add(self)
		self.image = image.convert()
		self.image.set_alpha(alpha)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.angle = 0
		self.width = width
		self.height = height
		self.active = False

class ActionPanel(GUIBaseClass):
	buttons = pygame.sprite.Group()
	active = None # TO HIGHLIGHT ACTIVE BUTTON
	def __init__(self, x, y, width, height, image):
		GUIBaseClass.__init__(self, x, y, width, height, image, 175)
		self.buttons.add(ZoningButton(self.rect.x + 10, self.rect.y + 20, BUTTON_WIDTH, BUTTON_HEIGHT, images.zoneButton))
		self.buttons.add(WallingButton(self.rect.x + 10, self.rect.y + BUTTON_HEIGHT + 40, BUTTON_WIDTH, BUTTON_HEIGHT, images.wallButton))
		active = None

	@staticmethod
	def updatePanel():
		for button in ActionPanel.buttons:
			if button == ActionPanel.active and not button.active:
				button.image.set_alpha(255)
				button.active = True
			elif button != ActionPanel.active and button.active:
				button.image.set_alpha(175)
				button.active = False

class ActionButton(ActionPanel):
	def __init__(self, x, y, width, height, image):
		GUIBaseClass.__init__(self, x, y, width, height, image, 175)
		#ActionPanel.buttons.add(self)
		
	def onClick(self):
		ActionPanel.active = self
		return

class WallingButton(ActionButton):
	def __init__(self, x, y, width, height, image):
		ActionButton.__init__(self, x, y, width, height, image)

	def onClick(self, builder):
		ActionPanel.active = self
		ActionPanel.updatePanel()
		builder.state = builder.WALL
		print "WALLING"

class ZoningButton(ActionButton):
	def __init__(self, x, y, width, height, image):
		ActionButton.__init__(self, x, y, width, height, image)

	def onClick(self, builder):
		ActionPanel.active = self
		ActionPanel.updatePanel()
		builder.state = builder.ZONE
		print "ZONING"
