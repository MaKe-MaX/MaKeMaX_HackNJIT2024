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
RED = (255, 0, 0)

bg = pygame.transform.scale(pygame.image.load(r"assets\backgrounds\orange_background.png"), (screen.get_width(), screen.get_height()))

# Load sprite sheets
sprite_sheet_walk = pygame.image.load(r"assets\player\hero_walking.png").convert_alpha()
sprite_sheet_idle = pygame.image.load(r"assets\player\hero_idle.png").convert_alpha()
sprite_sheet_attack = pygame.image.load(r"assets\player\hero_attack.png").convert_alpha()

# Automatically obtain sprite dimensions
sprite_height = sprite_sheet_walk.get_height()  # Get the dimensions of the entire sprite sheet
sprite_width = sprite_height
frame_count_walk = sprite_sheet_walk.get_width() // sprite_width  # Number of frames in the walking sprite sheet
frame_count_idle = sprite_sheet_idle.get_width() // sprite_width  # Number of frames in the idle sprite sheet
frame_count_attack = sprite_sheet_attack.get_width() // sprite_width  # Number of frames in the attack sprite sheet
animation_speed = 0.05  # Speed of animation (time per frame)
current_frame_walk = 0  # Track the current frame for walking
current_frame_idle = 0   # Track the current frame for idle
current_frame_attack = 0   # Track the current frame for attack
last_update_time = time.time()  # Track time for frame updates

# Scaling factor for the sprite frames
scale_factor = 2
scaled_sprite_width = sprite_width * scale_factor
scaled_sprite_height = sprite_height * scale_factor

# so that we can idle correctly
frame_rect = pygame.Rect(current_frame_idle * sprite_width, 0, sprite_width, sprite_height)
player_frame = sprite_sheet_idle.subsurface(frame_rect)
scaled_player_frame = pygame.transform.scale(player_frame, (scaled_sprite_width, scaled_sprite_height))

# Player settings
rect_x = 400  # Fixed horizontal position
rect_y = 300  # Starting vertical position
movement_scale = 0.006  # Adjust this to scale movement to the screen size

# Charging bar settings
charge_level = 0           # Current charge level
max_charge = 100           # Maximum charge level
charge_speed = 1           # Speed at which the bar fills
charge_bar_width = sprite_width
charge_bar_height = 10     # Height of the charging bar
charge_bar_y_offset = 20   # Distance above the rectangle for the bar
charge_bar_color = GREEN

# Jump and gravity settings
is_jumping = False
jump_velocity = 7  # Initial velocity for the jump
gravity = 0.1      # Gravity force pulling the rectangle down
vertical_velocity = 0  # Current vertical velocity of the rectangle

# Attack state
attacking = False  # Whether the player is attacking
attack_frame_duration = 0.5  # Duration for the attack animation
attack_start_time = 0  # Time when the attack starts

# Main loop
running = True
flipped = False
move_x, move_y, buttonOn, dist, distList, data = 0, 0, 0, 0, [0], []
while running:
    try:
        data = serial.read()  # Read joystick data
        move_x, move_y, buttonOn = data[0], data[1], data[2]

        # Only update `dist` if the fourth element is not zero
        if data[3] != 0:
            distList.append(data[3])
            if len(distList) > 5:
                distList.pop(0)
            dist = sum(distList) / len(distList)
    except:
        pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Horizontal movement
    rect_x = min(800 - sprite_width, max(0, rect_x + move_x * movement_scale))

    # Jump mechanics
    if not is_jumping and move_y < -480:  # Start jump if joystick pulled up
        is_jumping = True
        vertical_velocity = -jump_velocity  # Move up with initial velocity

    # Apply gravity if jumping
    if is_jumping:
        rect_y += vertical_velocity  # Update vertical position
        vertical_velocity += gravity  # Apply gravity to the velocity
        
        # Stop jumping if on the ground
        if rect_y >= 600 - sprite_height:
            rect_y = 600 - sprite_height  # Reset to ground level
            is_jumping = False          # End the jump
            vertical_velocity = 0       # Reset vertical velocity

    # Attack when full bar
    if charge_level == max_charge and dist <= 40:
        charge_bar_color = RED
        if dist <= 15:
            charge_level = 0
            attacking = True
            attack_start_time = time.time()  # Start the attack animation timer
    # Filling bar logic
    elif 15 <= dist <= 40:
        charge_level = min(max_charge, charge_level + charge_speed)  # Increment charge level
        charge_bar_color = GREEN
    else:
        charge_level = max(0, charge_level - charge_speed)  # Reset charge if out of range
        charge_bar_color = GREEN

    # Attack animation logic
    if attacking:
        if time.time() - attack_start_time < attack_frame_duration:
            if time.time() - last_update_time > animation_speed:
                current_frame_attack = (current_frame_attack + 1) % frame_count_attack  # Cycle through attack frames
                last_update_time = time.time()
            # Extract the current frame from the attack sprite sheet and scale it
            frame_rect = pygame.Rect(current_frame_attack * sprite_width, 0, sprite_width, sprite_height)
            player_frame = sprite_sheet_attack.subsurface(frame_rect)
            scaled_player_frame = pygame.transform.scale(player_frame, (scaled_sprite_width, scaled_sprite_height))
            scaled_player_frame = pygame.transform.flip(scaled_player_frame, flipped, False)
        else:
            attacking = False  # End the attack animation after duration
            current_frame_attack = 0  # Reset to the first frame of the attack animation
    else:
        # Determine if moving or idle
        if move_x != 0:  # If moving
            if current_frame_idle != 0:  # Reset idle frame if switching to walking
                current_frame_idle = 0  # Reset the idle animation frame when starting to walk
            if time.time() - last_update_time > animation_speed:
                current_frame_walk = (current_frame_walk + 1) % frame_count_walk  # Cycle through walking frames
                last_update_time = time.time()

            # Extract the current frame from the walking sprite sheet and scale it
            frame_rect = pygame.Rect(current_frame_walk * sprite_width, 0, sprite_width, sprite_height)
            player_frame = sprite_sheet_walk.subsurface(frame_rect)
            # Flip image if moving left
            scaled_player_frame = pygame.transform.scale(player_frame, (scaled_sprite_width, scaled_sprite_height))
            scaled_player_frame = pygame.transform.flip(scaled_player_frame, move_x < 0, False)
            if move_x < 0:
                flipped = True
            elif move_x > 0:
                flipped = False
        else:  # If idle
            if current_frame_walk != 0:  # Reset walking frame if switching to idle
                current_frame_walk = 0  # Reset the walking animation frame when starting to idle
            if time.time() - last_update_time > animation_speed:
                current_frame_idle = (current_frame_idle + 1) % frame_count_idle  # Cycle through idle frames
                last_update_time = time.time()
                # Flip image if flipped is true
                scaled_player_frame = pygame.transform.scale(player_frame, (scaled_sprite_width, scaled_sprite_height))
                scaled_player_frame = pygame.transform.flip(scaled_player_frame, flipped, False)

            # Extract the current frame from the idle sprite sheet and scale it
            frame_rect = pygame.Rect(current_frame_idle * sprite_width, 0, sprite_width, sprite_height)
            player_frame = sprite_sheet_idle.subsurface(frame_rect)

    # Calculate the new position to center the scaled image
    draw_x = rect_x + (sprite_width - scaled_sprite_width) // 2
    draw_y = rect_y + (sprite_height - scaled_sprite_height) // 2

    # Clear the screen
    screen.fill(BLACK)
    
    screen.blit(bg, (0,0))
    # Draw the player (scaled animated sprite) centered
    screen.blit(scaled_player_frame, (draw_x, draw_y))

    # Draw the charging bar above the player only if not attacking
    if not attacking:
        charge_bar_x = rect_x
        charge_bar_y = rect_y - charge_bar_y_offset
        pygame.draw.rect(screen, charge_bar_color, (charge_bar_x, charge_bar_y, charge_level / max_charge * charge_bar_width, charge_bar_height))

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
