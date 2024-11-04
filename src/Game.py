import pygame
import time
import src.serialfr as ser

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (206, 112, 43)
BLUE = (6, 222, 242)

class Game:

    def __init__(self, controller):   

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))  # Set screen dimensions
        pygame.display.set_caption("SteamPunch")
        if controller:
            self.serial = ser.serialfr()