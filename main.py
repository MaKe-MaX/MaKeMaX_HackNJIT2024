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
ORANGE = (206, 112, 43)

bg = pygame.transform.scale(pygame.image.load(r"assets\backgrounds\orange_background.png"), (screen.get_width(), screen.get_height()))

# Load sprite sheets
sprite_sheet_walk = pygame.image.load(r"assets\player\hero_walking.png").convert_alpha()
sprite_sheet_idle = pygame.image.load(r"assets\player\hero_idle.png").convert_alpha()
sprite_sheet_attack = pygame.image.load(r"assets\player\hero_attack.png").convert_alpha()

# Jump and gravity settings
is_jumping = False
jump_velocity = 7  # Initial velocity for the jump
gravity = 0.1      # Gravity force pulling the rectangle down
vertical_velocity = 0  # Current vertical velocity of the rectangle

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
rect_y = 0  # Starting vertical position
movement_scale = 0.006  # Adjust this to scale movement to the screen size

# Charging bar settings
charge_level = 0           # Current charge level
max_charge = 100           # Maximum charge level
charge_speed = 1           # Speed at which the bar fills
charge_bar_width = sprite_width
charge_bar_height = 10     # Height of the charging bar
charge_bar_y_offset = 20   # Distance above the rectangle for the bar
charge_bar_color = GREEN

# Attack state
player_attacking = False  # Whether the player is player_attacking
attack_framef_duration = 0.5  # Duration for the attack animation
attack_start_time = 0  # Time when the attack starts

# Define platforms the player can jump through from below
platforms = [pygame.Rect(300, 400, 200, 20), pygame.Rect(100, 300, 150, 20), pygame.Rect(5, 600, 800, 20)]

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
    rect_x = min(800 - 3*sprite_width/4-6, max(-sprite_width/4+6, rect_x + move_x * movement_scale))

   # Jump mechanics
    if not is_jumping and move_y < -480:  # Start jump if joystick pulled up
        is_jumping = True
        vertical_velocity = -jump_velocity  # Move up with initial velocity

    # Apply gravity if jumping
    if is_jumping:
        rect_y += vertical_velocity  # Update vertical position
        vertical_velocity += gravity  # Apply gravity to the velocity

    # Platform collision detection
    on_platform = False  # Track if player is on any platform

    for platform in platforms:
        # Check if the player is landing on a platform
        if vertical_velocity > 0 and rect_y + sprite_height <= platform.top and rect_y + sprite_height + vertical_velocity >= platform.top:
            if rect_x + 3*sprite_width/4.5 > platform.left and rect_x + sprite_width/3.5 < platform.right:
                rect_y = platform.top - sprite_height
                vertical_velocity = 0
                is_jumping = False
                on_platform = True  # Mark as on platform
                break

    # Set to falling if not on any platform
    if not on_platform:
        is_jumping = True


    # Attack when full bar
    if charge_level == max_charge and dist <= 40:
        charge_bar_color = RED
        if dist <= 15:
            charge_level = 0
            player_attacking = True
            attack_start_time = time.time()
    elif 15 <= dist <= 40:
        charge_level = min(max_charge, charge_level + charge_speed)
        charge_bar_color = GREEN
    else:
        charge_level = max(0, charge_level - charge_speed)
        charge_bar_color = GREEN

    # Player Character: Animation logic (walking, idle, attack)
    if player_attacking:
        if time.time() - attack_start_time < attack_frame_duration:
            if time.time() - last_update_time > animation_speed:
                current_frame_attack = (current_frame_attack + 1) % frame_count_attack
                last_update_time = time.time()
            frame_rect = pygame.Rect(current_frame_attack * sprite_width, 0, sprite_width, sprite_height)
            player_frame = sprite_sheet_attack.subsurface(frame_rect)
            scaled_player_frame = pygame.transform.scale(player_frame, (scaled_sprite_width, scaled_sprite_height))
            scaled_player_frame = pygame.transform.flip(scaled_player_frame, flipped, False)
        else:
            player_attacking = False
            current_frame_attack = 0
    else:
        if move_x != 0:
            if current_frame_idle != 0:
                current_frame_idle = 0
            if time.time() - last_update_time > animation_speed:
                current_frame_walk = (current_frame_walk + 1) % frame_count_walk
                last_update_time = time.time()
            frame_rect = pygame.Rect(current_frame_walk * sprite_width, 0, sprite_width, sprite_height)
            player_frame = sprite_sheet_walk.subsurface(frame_rect)
            scaled_player_frame = pygame.transform.scale(player_frame, (scaled_sprite_width, scaled_sprite_height))
            scaled_player_frame = pygame.transform.flip(scaled_player_frame, move_x < 0, False)
            flipped = move_x < 0
        else:
            if current_frame_walk != 0:
                current_frame_walk = 0
            if time.time() - last_update_time > animation_speed:
                current_frame_idle = (current_frame_idle + 1) % frame_count_idle
                last_update_time = time.time()
            frame_rect = pygame.Rect(current_frame_idle * sprite_width, 0, sprite_width, sprite_height)
            player_frame = sprite_sheet_idle.subsurface(frame_rect)
            scaled_player_frame = pygame.transform.scale(player_frame, (scaled_sprite_width, scaled_sprite_height))
            scaled_player_frame = pygame.transform.flip(scaled_player_frame, flipped, False)


    # Enemy 1: Animation logic (walking, idle, attack)
    # Player Character: Animation logic (walking, idle, attack)
    
    if player_attacking:
        if time.time() - attack_start_time < attack_frame_duration:
            if time.time() - last_update_time > animation_speed:
                current_frame_attack = (current_frame_attack + 1) % frame_count_attack
                last_update_time = time.time()
            frame_rect = pygame.Rect(current_frame_attack * sprite_width, 0, sprite_width, sprite_height)
            player_frame = sprite_sheet_attack.subsurface(frame_rect)
            scaled_player_frame = pygame.transform.scale(player_frame, (scaled_sprite_width, scaled_sprite_height))
            scaled_player_frame = pygame.transform.flip(scaled_player_frame, flipped, False)
        else:
            player_attacking = False
            current_frame_attack = 0
    else:
        if move_x != 0:
            if current_frame_idle != 0:
                current_frame_idle = 0
            if time.time() - last_update_time > animation_speed:
                current_frame_walk = (current_frame_walk + 1) % frame_count_walk
                last_update_time = time.time()
            frame_rect = pygame.Rect(current_frame_walk * sprite_width, 0, sprite_width, sprite_height)
            player_frame = sprite_sheet_walk.subsurface(frame_rect)
            scaled_player_frame = pygame.transform.scale(player_frame, (scaled_sprite_width, scaled_sprite_height))
            scaled_player_frame = pygame.transform.flip(scaled_player_frame, move_x < 0, False)
            flipped = move_x < 0
        else:
            if current_frame_walk != 0:
                current_frame_walk = 0
            if time.time() - last_update_time > animation_speed:
                current_frame_idle = (current_frame_idle + 1) % frame_count_idle
                last_update_time = time.time()
            frame_rect = pygame.Rect(current_frame_idle * sprite_width, 0, sprite_width, sprite_height)
            player_frame = sprite_sheet_idle.subsurface(frame_rect)
            scaled_player_frame = pygame.transform.scale(player_frame, (scaled_sprite_width, scaled_sprite_height))
            scaled_player_frame = pygame.transform.flip(scaled_player_frame, flipped, False)
           


    # Calculate position to center the scaled image
    draw_x = rect_x + (sprite_width - scaled_sprite_width) // 2
    draw_y = rect_y + (sprite_height - scaled_sprite_height) // 2

    # Clear the screen
    screen.blit(bg, (0, 0))

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, BLACK, platform)

    # Draw the player
    screen.blit(scaled_player_frame, (draw_x, draw_y))

    # Draw the charge bar
    if not player_attacking:
        charge_bar_x = rect_x
        charge_bar_y = rect_y - charge_bar_y_offset
        pygame.draw.rect(screen, charge_bar_color, (charge_bar_x, charge_bar_y, charge_level / max_charge * charge_bar_width, charge_bar_height))

    pygame.display.flip()

pygame.quit()
