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

pygame.init()
pygame.display.init()

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
FPS = 50
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

for i in xrange(1, 10):
	c = Customer(30 * i, 150, 30, 30, images.customer)

Truck(600, 495, 60, 30, images.truck)



panel = ActionPanel(0, 10, 60, 400, images.panel)
# UNITS

# print "Startup took: " + str((time.clock() * 1000) - t1)

# ---------- MAIN GAME LOOP -------------
while True:
	totalFrames += 1
	process(god)	
	god.update()
	panel.updatePanel()

	#LOGIC
	for zone in Terrain.zones:
		zone.update()

	for tile in Terrain.List:
		tile.motion(god.cameraX, god.cameraY)

	for b in Box.List:
		b.motion(god.cameraX, god.cameraY)
		if b.getCurrentTile() and not b.getCurrentTile().zone == Terrain.DELIVERABLES and not b.awaitingOwner and not b.owner:
			moveTo = Terrain.getVacantTileInZone(Terrain.DELIVERABLES)
			if moveTo:
				b.awaitingOwner = True
				TaskManager.addTask(Task.MOVE_OBJECT, b.getCurrentTile(), moveTo, b)

	for c in Customer.List:
		if c.task == None:
			if not TaskManager.isEmpty():
				c.assignTask(TaskManager.takeTask())
		c.motion(god.cameraX, god.cameraY)
		c.update(grid)

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
		for c in Customer.List:
			c.setTargetTile(c.targetTile, grid)	
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

	pygame.display.flip()	
	#DRAW

	#LOGIC
	clock.tick(FPS)
	#LOGIC