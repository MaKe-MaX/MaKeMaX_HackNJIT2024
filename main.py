import pygame
import time
import src.serialfr as ser


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600)) # Set screen dimensions
pygame.display.set_caption("Our Game")

serial = ser.serialfr()

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

time.sleep(2)  # Wait for the serial connection to initialize

# Rectangle settings
rect_x = 400  # Fixed horizontal position
rect_y = 300  # Starting vertical position
rect_width = 50
rect_height = 50
movement_scale = 0.002  # Adjust this to scale movement to the screen size

# Main loop
running = True
while running:
    data = []
    move_x, move_y, buttonOn, dist = serial.read()
    #print(move_x, move_y, buttonOn, dist)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    rect_x += move_x * movement_scale  # Map distance to screen width
    rect_y +=  move_y * movement_scale  # Map distance to screen height

    # Clear the screen
    screen.fill(BLACK)

    # Draw the rectangle
    pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_width, rect_height))

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
