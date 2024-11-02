import pygame
import serial
import time


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600)) # Set screen dimensions
pygame.display.set_caption("Our Game")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the serial port
ser = serial.Serial('COM5', 19200, timeout=1)
time.sleep(2)  # Wait for the serial connection to initialize

# Rectangle settings
rect_x = 400  # Fixed horizontal position
rect_y = 300  # Starting vertical position
rect_width = 50
rect_height = 50
movement_scale = 0.2  # Adjust this to scale movement to the screen size

# Main loop
running = True
while running:
    data = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if ser.in_waiting > 0:
        try:
            distance = int(ser.readline().decode().strip())  # Read and parse the distance value
            rect_y = max(0, min(600 - rect_height, distance * movement_scale))  # Map distance to screen height
        except ValueError:
            pass  # Ignore any parsing errors

    # Clear the screen
    screen.fill(BLACK)

    # Draw the rectangle
    pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_width, rect_height))

    # Update the display
    pygame.display.flip()
    pygame.time.delay(30)  # Delay to control frame rate

# Clean up
ser.close()
pygame.quit()
