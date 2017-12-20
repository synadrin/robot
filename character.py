import pygame
import spritesheet

class character(pygame.sprite.Sprite):
	""" Character

	Characters have three collision rects, one for the whole sprite "rect" and
	"old_rect", and another to check collisions with walls, called "feet".

	The position list is used because pygame rects are inaccurate for
	positioning sprites; because the values they get are 'rounded down'
	as integers, the sprite would move faster moving left or up.

	Feet is 1/2 as wide as the normal rect, and 8 pixels tall.  This size size
	allows the top of the sprite to overlap walls.  The feet rect is used for
	collisions, while the 'rect' rect is used for drawing.

	There is also an old_rect that is used to reposition the sprite if it
	collides with level walls.
	"""

	def __init__(self, filename, width, height, speed):
		pygame.sprite.Sprite.__init__(self)
		self._speed = speed

		self._spritesdown = spritesheet.spritestripanim(
			filename, (0, 0, width, height),
			4, (0, 255, 0), True, speed / 10
		)
		self._spritesleft = spritesheet.spritestripanim(
			filename, (0, height, width, height),
			4, (0, 255, 0), True, speed / 10
		)
		self._spritesright = spritesheet.spritestripanim(
			filename, (0, 2 * height, width, height),
			4, (0, 255, 0), True, speed / 10
		)
		self._spritesup = spritesheet.spritestripanim(
			filename, (0, 3 * height, width, height),
			4, (0, 255, 0), True, speed / 10
		)
		self.image = self._spritesdown.next()
		self.velocity = [0, 0]
		self._position = [0, 0]
		self._old_position = self.position
		self.rect = self.image.get_rect()
		self.feet = pygame.Rect(0, 0, self.rect.width * .5, 8)

	@property
	def position(self):
		return list(self._position)

	@position.setter
	def position(self, value):
		self._position = list(value)

	def update(self, dt):
		self._old_position = self._position[:]
		self._position[0] += self.velocity[0] * dt
		self._position[1] += self.velocity[1] * dt
		self.rect.topleft = self._position
		self.feet.midbottom = self.rect.midbottom

	def move_back(self, dt):
		""" If called after an update, the sprite can move back
		"""
		self._position = self._old_position
		self.rect.topleft = self._position
		self.feet.midbottom = self.rect.midbottom

	def stop_moving_vertical(self):
		self.velocity[1] = 0

	def move_up(self):
		self.velocity[1] = -self._speed
		self.image = self._spritesup.next()

	def move_down(self):
		self.velocity[1] = self._speed
		self.image = self._spritesdown.next()

	def stop_moving_horizontal(self):
		self.velocity[0] = 0

	def move_left(self):
		self.velocity[0] = -self._speed
		self.image = self._spritesleft.next()
	
	def move_right(self):
		self.velocity[0] = self._speed
		self.image = self._spritesright.next()
