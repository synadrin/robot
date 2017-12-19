# https://learn.adafruit.com/pi-video-output-using-pygame/pointing-pygame-to-the-framebuffer

import os
import pygame
import time
from constants import *

class pyscope:
	screen = None;
	
	def resize(self, width, height):
		self.screen = pygame.display.set_mode(
			(width, height), pygame.RESIZABLE)

	def __init__(self):
		"Ininitializes a new pygame screen using the framebuffer"
		# Based on "Python GUI in Linux frame buffer"
		# http://www.karoltomala.com/blog/?p=679
		display = os.getenv('DISPLAY')
		if display:
			print("Display: {0}".format(display))
			self.resize(DISPLAY_WIDTH, DISPLAY_HEIGHT)
			pygame.display.set_caption(DISPLAY_NAME)
		
		else:
			os.putenv('SDL_FBDEV', DISPLAY_FBDEV)
			# Check which frame buffer drivers are available
			# Start with fbcon since directfb hangs with composite output
			drivers = ['fbcon', 'directfb', 'svgalib']
			found = False
			for driver in drivers:
				# Make sure that SDL_VIDEODRIVER is set
				if not os.getenv('SDL_VIDEODRIVER'):
					os.putenv('SDL_VIDEODRIVER', driver)
				try:
					pygame.display.init()
				except pygame.error:
					print('Driver: {0} failed.'.format(driver))
					continue
				found = True
				break
	
			if not found:
				raise Exception('No suitable video driver found!')
		
			size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
			print("Display: Framebuffer (%d x %d)" % (size[0], size[1]))
			self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

		# Clear the screen to start
		self.screen.fill((0, 0, 0))		
		# Disable mouse
		pygame.mouse.set_visible(False)
		# Initialise font support
		pygame.font.init()
		# Render the screen
		pygame.display.update()
 
	def __del__(self):
		"Destructor to make sure pygame shuts down, etc."
 
	def test(self):
		# Fill the screen with red (255, 0, 0)
		red = (255, 0, 0)
		self.screen.fill(red)
		# Update the display
		pygame.display.update()
 

if __name__ == '__main__':
	# Create an instance of the PyScope class
	scope = pyscope()
	scope.test()
	time.sleep(10)
