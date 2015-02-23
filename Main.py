import pygame, sys, math, random, time, images
from classes import *
from gui import *
from maps import *
from builder import *
from ai import AI
from process import *
from God import *
from zone import *

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
print "Startup took: " + str((time.clock() * 1000) - t1)
# MISC

# UNITS
god = God()

#for i in xrange(1, 3):
Customer(150, 150, 30, 30, images.customer)
rooms = []
Truck(1920, 495, 60, 30, images.truck)

panel = ActionPanel(0, 10, 60, 400, images.panel)
# UNITS


# ---------- MAIN GAME LOOP -------------
while True:
	totalFrames += 1
	process(god)	
	god.update()

	#LOGIC
	for zone in Terrain.zones:
		zone.update()

	for tile in Terrain.List:
		tile.motion(god.cameraX, god.cameraY)

	for c in Customer.List:
		if not c.targetSet:
			x = (int)(random.random() * (TILES_WIDTH * TILE_SIZE))
			y = (int)(random.random() * (TILES_WIDTH * TILE_SIZE)) 
			obj = Collision.getObjectAt(Terrain.List, x, y)
			if obj != None:
				c.setTarget(obj, grid)

		c.motion(god.cameraX, god.cameraY)
		c.update()

	for t in Truck.List:
		t.motion(god.cameraX, god.cameraY)
		t.update()

	tX, tY = pygame.mouse.get_pos()
	x, y = tX + god.cameraX, tY + god.cameraY
	builder.drawBuildPath(x, y)
	builder.drawRemovePath(x, y)

	if builder.builtSinceLastLoop:
		matrix = grid.update(Terrain.List, god.cameraX, god.cameraY)
		grid.orientWalls(matrix, Terrain.List, god.cameraX, god.cameraY)
		builder.builtSinceLastLoop = False
		for c in Customer.List:
			c.setTarget(c.targetTile, grid)	


	#LOGIC

	#COLLISION 

	#COLLISION 

	#MISC

	#MISC

	#DRAW
	screen.fill((255, 255, 255))
	BaseClass.backgroundSprites.draw(screen)
	BaseClass.foregroundSprites.draw(screen)
	GUIBaseClass.allSprites.draw(screen)
	pygame.display.flip()	
	#DRAW

	#LOGIC
	clock.tick(FPS)
	#LOGIC