import pygame

class sprite:
	@staticmethod
	def getSprite(source, rect):
		img = source
		img.set_clip(rect)
		return img.subsurface(img.get_clip())

	@staticmethod
	def getSpriteSheet(source, rect, qty):
		img = source
		output = {}
		x, y, w, h = rect
		for i in xrange(0, qty):
			img.set_clip((x + (i * w), y, w, h))
			output[i] = img.subsurface(img.get_clip())
		return output
