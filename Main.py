import pygame, sys, math, random, time, images
from classes import *
from gui import *
from maps import *
from builder import *
from ai import AI
from process import *
from God import *
from zone import *
from taskManager import *
from player import *

pygame.display.init()
pygame.init()


t1 = time.clock() * 1000
# SETTINGS

FULLSCREEN = False
if FULLSCREEN:
	screenInfo = pygame.display.Info()
	SCREEN_WIDTH, SCREEN_HEIGHT = screenInfo.current_w, screenInfo.current_h
	FLAGS = pygame.FULLSCREEN | pygame.DOUBLEBUF
else: 
	SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
	FLAGS = pygame.DOUBLEBUF

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FLAGS, 32)
clock = pygame.time.Clock()
pygame.display.set_caption('The Computer Shop Game')
FPS = 100
fiveSecondinterval = FPS * 5
totalFrames = 0
# SETTINGS

# TERRAIN
TILE_SIZE = 30
TILES_WIDTH = 20
TILES_HEIGHT = 20
matrix = [[0 for i in xrange(TILES_WIDTH)] for i in xrange(TILES_HEIGHT)]
matrix = loadMap(matrix)
# matrix = createMap(matrix)
generateMap(matrix)
#TERRAIN

# AI
grid = GridWithWeights(matrix)
# AI

# MISC

# MISC


# UNITS
god = God()

for i in xrange(1, 20):
	c = Customer(TILE_SIZE * i, 150, 30, 30, images.customer)

Truck(600, 495, 60, 30, images.truck)



#panel = ActionPanel(0, 10, 60, 400, images.panel)
# UNITS

# print "Startup took: " + str((time.clock() * 1000) - t1)

# ---------- MAIN GAME LOOP -------------
while True:
	totalFrames += 1
	process(god)	
	god.update()
	#panel.updatePanel()

	#LOGIC
	for zone in Terrain.zones:
		zone.update()

	for tile in Terrain.List:
		tile.motion(god.cameraX, god.cameraY)

	for b in Book.List:
		if b.mustUpdate or god.movedSinceLastLoop:
			b.motion(god.cameraX, god.cameraY)

	for b in Box.List:
		if b.mustUpdate or god.movedSinceLastLoop:
			b.motion(god.cameraX, god.cameraY)
		if Terrain.vacantTiles[Terrain.DELIVERABLES] > 0:
			if b.currentTile and not b.currentTile.zone == Terrain.DELIVERABLES and not b.awaitingOwner and not b.owner:
				moveTo = Terrain.getVacantTileInZone(Terrain.DELIVERABLES)
				if moveTo:
					b.awaitingOwner = True
					TaskManager.addTask(Task.MOVE_OBJECT, b.currentTile, moveTo, b, Terrain.DELIVERABLES)

	for c in Customer.List:
		if not c.task:
			if not TaskManager.isEmpty():
				c.assignTask(TaskManager.takeTask())
		c.motion(god.cameraX, god.cameraY)
		c.update(grid)
		if builder.builtSinceLastLoop:
			c.setTargetTile(c.targetTile, grid)	

	for t in Truck.List:
		t.motion(god.cameraX, god.cameraY)
		t.update()

	x, y = pygame.mouse.get_pos()
	
	builder.drawBuildPath(x, y)
	builder.drawRemovePath(x, y)

	if builder.builtSinceLastLoop:
		matrix = grid.update(Terrain.List, god.cameraX, god.cameraY)
		grid.orientWalls(matrix, Terrain.List, god.cameraX, god.cameraY)
		builder.builtSinceLastLoop = False

	#LOGIC


	#COLLISION 

	#COLLISION 

	#MISC

	#MISC

	#DRAW
	try:
		screen.fill((255, 255, 255))
		BaseClass.backgroundSprites.draw(screen)
		BaseClass.foregroundSprites.draw(screen)
		GUIBaseClass.allSprites.draw(screen)
	except KeyError:
		print "~error: KeyError, when drawing something :("

	pygame.display.update()	
	#DRAW

	#LOGIC
	clock.tick(FPS)
	if totalFrames % 5 == 0:
		print clock.get_fps()
	#LOGIC