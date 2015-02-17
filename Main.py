import pygame, sys, math, random, time
import images
from classes import *
from gui import *
from maps import *
from builder import *
from ai import AI
from process import *
from God import *

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
screen.set_alpha(None)
clock = pygame.time.Clock()
FPS = 40
fiveSecondinterval = FPS * 5
totalFrames = 0
# SETTINGS

# TERRAIN
TILE_SIZE = 30
TILES_WIDTH = 42
TILES_HEIGHT = 24
matrix = [[0 for i in xrange(TILES_WIDTH)] for i in xrange(TILES_HEIGHT)]
matrix = loadMap(matrix)

# matrix = createMap(matrix)
generateMap(matrix)
#TERRAIN

# AI
grid = GridWithWeights(matrix)
# AI
print "Startup took: " + str((time.clock() * 1000) - t1)
# MISC
# MISC

# UNITS
god = God()

#for i in xrange(1, 3):
#	Customer(150, 150, 30, 30, images.customer)

Truck(1920, 495, 60, 30, images.truck)

#panel = ActionPanel(0, 10, 60, 400, images.panel)
# UNITS



# ---------- MAIN GAME LOOP -------------

# FLOOD ROOM AND REPAINT
# TODO: MOVE
s = Collision.getObjectAt(Terrain.List, 50, 100)
room = builder.floodRoom(s, Terrain.List)
for r in room:
	r.image = images.grayScaleFloor

while True:
	totalFrames += 1
	process(god)	
	god.update()

	for c in Customer.List:
		x = (int)(random.random() * SCREEN_WIDTH)
		y = (int)(random.random() * SCREEN_HEIGHT)

		obj = Collision.getObjectAt(Terrain.List, x, y)
		if obj != None and c.targetSet == False:
			c.setTarget(obj, grid)

	#LOGIC
	for tile in Terrain.List:
		tile.motion(god.CAMERA_X, god.CAMERA_Y)

	for c in Customer.List:
		c.motion(god.CAMERA_X, god.CAMERA_Y)
		c.update()

	for t in Truck.List:
		t.motion(god.CAMERA_X, god.CAMERA_Y)
		t.update()

	tX, tY = pygame.mouse.get_pos()
	x, y = tX + god.CAMERA_X, tY + god.CAMERA_Y
	builder.drawBuildPath(x, y)
	builder.drawRemovePath(x, y)
	grid.update(Terrain.List)

	if builder.builtSinceLastLoop:
		matrix = grid.update(Terrain.List)
		grid.orientWalls(matrix, Terrain.List)
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