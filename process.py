import gui, pygame, sys
from builder import *
from zone import *

def process(god):
	for event in pygame.event.get():  
		if event.type == pygame.QUIT:  
			pygame.quit()  
			sys.exit() 	

		if event.type == pygame.MOUSEBUTTONDOWN:
			x, y = pygame.mouse.get_pos()

			clickedTile = Collision.getObjectAt(gui.GUIBaseClass.allSprites, x, y)
			if clickedTile == None:
				builder.onMouseDown(x, y, event)

		if event.type == pygame.MOUSEBUTTONUP:
				x, y = pygame.mouse.get_pos()

				builder.onMouseRelease(x, y, event)

				button = Collision.getObjectAt(gui.ActionPanel.buttons, x, y) 
				if button:
					button.onClick(builder)


		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_1:
				builder.state = builder.ZONE
			if event.key == pygame.K_2:
				builder.state = builder.WALL
			if event.key == pygame.K_3:
				builder.state = builder.INACTIVE
			if event.key == pygame.K_4:
				print 4
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
			if event.key == pygame.K_w:
				god.key_w = True

			if event.key == pygame.K_s:
				god.key_s = True

			if event.key == pygame.K_d:
				god.key_d = True

			if event.key == pygame.K_a:
				god.key_a = True

			if event.key == pygame.K_LSHIFT:
				god.key_LSHIFT = True

		if event.type == pygame.KEYUP:		
			if event.key == pygame.K_w:
				god.key_w = False

			if event.key == pygame.K_s:
				god.key_s = False

			if event.key == pygame.K_d:
				god.key_d = False

			if event.key == pygame.K_a:
				god.key_a = False

			if event.key == pygame.K_LSHIFT:
				god.key_LSHIFT = False
