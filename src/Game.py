import pygame
import time
import src.serialfr as ser

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (206, 112, 43)

class Game:

    def __init__(self):   

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))  # Set screen dimensions
        pygame.display.set_caption("Our Game")

        self.serial = ser.serialfr()

        self.bg = pygame.transform.scale(pygame.image.load(r"assets\backgrounds\orange_background.png"), (self.screen.get_width(), self.screen.get_height()))

