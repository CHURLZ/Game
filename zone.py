import images, pygame
from classes import Terrain

TILE_SIZE = 30

class Zone():
	def __init__(self, startPos):
		self.tiles = []
		self.startPos = startPos

		self.inLimbo = True

	def update(self):
		# TODO: change to update on mouse movement event
		if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
			if self.inLimbo:
				self.drawBuildArea(Terrain.List, pygame.mouse.get_pos())

	def onMouseRelease(self, tiles, endPos):
		self.setMatrixCoords(endPos)
		self.setTiles(tiles)

		self.inLimbo = False

	def setTiles(self, tiles):
		for tile in tiles:
			if tile.walkable and self.__inRange(tile.rect, (self.originX, self.originY), (self.endX, self.endY)):
				self.tiles.append(tile)
				tile.image = images.greenFloor


	def setMatrixCoords(self, endPos):
		x1, y1 = self.startPos
		x2, y2 = endPos
		if x1 < x2:
			self.originX = x1
			self.endX = x2
		else:
			self.originX = x2
			self.endX = x1

		if y1 < y2:
			self.originY = y1
			self.endY = y2
		else:
			self.originY = y2
			self.endY = y1

	def drawBuildArea(self, tiles, (mouseX, mouseY)):
		for tile in self.tiles:
			tile.image = tile.default_image
		for tile in tiles:
			if self.__inRange(tile.rect, self.startPos, (mouseX, mouseY)):
				self.tiles.append(tile)
				tile.image = images.greenFloor



	def __inRange(self, rect, (x1, y1), (x2, y2)):
		if x1 < x2:
			lowX = x1
			highX = x2
		else:
			highX = x1
			lowX = x2
		if y1 < y2:
			lowY = y1
			highY = y2
		else:
			highY = y1
			lowY = y2

		if rect.x + TILE_SIZE > lowX and rect.x < highX and rect.y + TILE_SIZE > lowY and rect.y < highY:
			return True
		else: 
			return False