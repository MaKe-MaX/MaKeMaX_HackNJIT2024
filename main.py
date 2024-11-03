import pygame
import time
import src.serialfr as ser

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))  # Set screen dimensions
pygame.display.set_caption("Our Game")

serial = ser.serialfr()

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

time.sleep(2)  # Wait for the serial connection to initialize

# Rectangle settings
rect_x = 400  # Fixed horizontal position
rect_y = 300  # Starting vertical position
rect_width = 50
rect_height = 50
movement_scale = 0.006  # Adjust this to scale movement to the screen size

# Charging bar settings
charge_level = 0           # Current charge level
max_charge = 100           # Maximum charge level
charge_speed = 1           # Speed at which the bar fills
charge_bar_width = rect_width
charge_bar_height = 10     # Height of the charging bar
charge_bar_y_offset = 20   # Distance above the rectangle for the bar

# Jump and gravity settings
is_jumping = False
jump_velocity = 7  # Initial velocity for the jump
gravity = 0.1      # Gravity force pulling the rectangle down
vertical_velocity = 0  # Current vertical velocity of the rectangle

# Main loop
running = True
move_x, move_y, buttonOn, dist, distList = 0, 0, 0, 0, [0]
while running:
    try:
        data = serial.read()  # Read joystick data
        move_x, move_y, buttonOn = data[0], data[1], data[2]

        # Only update `dist` if the fourth element is not zero
        if data[3] != 0:
            distList.append(data[3])
            if len(distList) > 5:
                distList.pop(0)
            dist = sum(distList)/len(distList)
    except:
        pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Horizontal movement
    rect_x = min(800 - rect_width, max(0, rect_x + move_x * movement_scale))

    # Jump mechanics
    if not is_jumping and move_y < -480:  # Start jump if joystick pulled up
        is_jumping = True
        vertical_velocity = -jump_velocity  # Move up with initial velocity

    # Apply gravity if jumping
    if is_jumping:
        rect_y += vertical_velocity  # Update vertical position
        vertical_velocity += gravity  # Apply gravity to the velocity
        
        # Stop jumping if on the ground
        if rect_y >= 600 - rect_height:
            rect_y = 600 - rect_height  # Reset to ground level
            is_jumping = False          # End the jump
            vertical_velocity = 0       # Reset vertical velocity

    # Charging bar logic
    print(dist)
    if 15 <= dist and dist <= 40:
        print(1231234567890234567890123456789098765432456789)
        charge_level = min(max_charge, charge_level + charge_speed)  # Increment charge level
    else:
        charge_level -= charge_speed  # Reset charge if out of range

    # Clear the screen
    screen.fill(BLACK)

    # Draw the rectangle
    pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_width, rect_height))

    # Draw the charging bar above the rectangle
    charge_bar_x = rect_x
    charge_bar_y = rect_y - charge_bar_y_offset
    pygame.draw.rect(screen, GREEN, (charge_bar_x, charge_bar_y, charge_level / max_charge * charge_bar_width, charge_bar_height))

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
