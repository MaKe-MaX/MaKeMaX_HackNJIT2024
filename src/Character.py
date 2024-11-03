import pygame
import time


gravity = 0.1      # Gravity force pulling the rectangle down


class Character:
    def __init__(self, name):
        # Load sprite sheets
        self.sprite_sheet_walk = pygame.image.load(rf"assets\{name}_walking.png").convert_alpha()
        self.sprite_sheet_idle = pygame.image.load(rf"assets\{name}_idle.png").convert_alpha()
        self.sprite_sheet_attack = pygame.image.load(rf"assets\{name}_attack.png").convert_alpha()
        self.sprite_sheet_hit = pygame.image.load(rf"assets\{name}_whitehit.png").convert_alpha()
        self.sprite_sheet_death = pygame.image.load(rf"assets\{name}_death.png").convert_alpha()

        # Jump and gravity settings
        self.is_jumping = False
        self.flipped = False
        self.jump_velocity = 7  # Initial velocity for the jump
        self.vertical_velocity = 0  # Current vertical velocity of the rectangle

        # Automatically obtain sprite dimensions
        self.sprite_height = self.sprite_sheet_walk.get_height()  # Get the dimensions of the entire sprite sheet
        self.sprite_width = self.sprite_height
        self.frame_count_walk = self.sprite_sheet_walk.get_width() // self.sprite_width  # Number of frames in the walking sprite sheet
        self.frame_count_idle = self.sprite_sheet_idle.get_width() // self.sprite_width  # Number of frames in the idle sprite sheet
        self.frame_count_attack = self.sprite_sheet_attack.get_width() // self.sprite_width  # Number of frames in the attack sprite sheet
        self.current_frame_walk = 0  # Track the current frame for walking
        self.current_frame_idle = 0   # Track the current frame for idle
        self.current_frame_attack = 0   # Track the current frame for attack
        self.last_update_time = time.time()  # Track time for frame updates
        self.animation_speed = 0.05  # Speed of animation (time per frame)

        # Scaling factor for the sprite frames
        self.scale_factor = 2
        self.scaled_sprite_width = self.sprite_width * self.scale_factor
        self.scaled_sprite_height = self.sprite_height * self.scale_factor

        # so that we can idle correctly
        self.frame_rect = pygame.Rect(self.current_frame_idle * self.sprite_width, 0, self.sprite_width, self.sprite_height)
        self.player_frame = self.sprite_sheet_idle.subsurface(self.frame_rect)
        self.scaled_player_frame = pygame.transform.scale(self.player_frame, (self.scaled_sprite_width, self.scaled_sprite_height))

        # Automatically obtain sprite dimensions
        self.sprite_height = self.sprite_sheet_walk.get_height()  # Get the dimensions of the entire sprite sheet
        self.sprite_width = self.sprite_height

        # Player settings
        self.rect_x = 400  # Fixed horizontal position
        self.rect_y = 0  # Starting vertical position
        self.movement_scale = 0.006  # Adjust this to scale movement to the screen size
        self.draw_x = self.rect_x + (self.sprite_width - self.scaled_sprite_width) // 2
        self.draw_y = self.rect_y + (self.sprite_height - self.scaled_sprite_height) // 2

        # Attack states
        self.player_attacking = False  # Whether the player is player_attacking
        self.attack_frame_duration = 0.5  # Duration for the attack animation
        self.attack_start_time = 0  # Time when the attack starts


    def move(self, platforms, move_x, move_y):
    
         # Horizontal movement
        self.rect_x = min(800 - 3*self.sprite_width/4-6, max(-self.sprite_width/4+6, self.rect_x + move_x * self.movement_scale))

        # Jump mechanics
        if not self.is_jumping and move_y < -480:  # Start jump if joystick pulled up
            self.is_jumping = True
            self.vertical_velocity = -self.jump_velocity  # Move up with initial velocity

        # Apply gravity if jumping
        if self.is_jumping:
            self.rect_y += self.vertical_velocity  # Update vertical position
            self.vertical_velocity += gravity  # Apply gravity to the velocity

        # Platform collision detection
        on_platform = False  # Track if player is on any platform

        for platform in platforms:
            # Check if the player is landing on a platform
            if self.vertical_velocity > 0 and self.rect_y + self.sprite_height <= platform.top and self.rect_y + self.sprite_height + self.vertical_velocity >= platform.top:
                if self.rect_x + 3*self.sprite_width/4.5 > platform.left and self.rect_x + self.sprite_width/3.5 < platform.right:
                    self.rect_y = platform.top - self.sprite_height
                    self.vertical_velocity = 0
                    self.is_jumping = False
                    on_platform = True  # Mark as on platform
                    break

        # Set to falling if not on any platform
        if not on_platform:
            self.is_jumping = True

        
        self.draw_x = self.rect_x + (self.sprite_width - self.scaled_sprite_width) // 2
        self.draw_y = self.rect_y + (self.sprite_height - self.scaled_sprite_height) // 2


    def change_frame(self, move_x, move_y):
        # Player Character: Animation logic (walking, idle, attack)
        if self.player_attacking:
            if time.time() - self.attack_start_time < self.attack_frame_duration:
                if time.time() - self.last_update_time > self.animation_speed:
                    self.current_frame_attack = (self.current_frame_attack + 1) % self.frame_count_attack
                    self.last_update_time = time.time()
                self.frame_rect = pygame.Rect(self.current_frame_attack * self.sprite_width, 0, self.sprite_width, self.sprite_height)
                self.player_frame = self.sprite_sheet_attack.subsurface(self.frame_rect)
                self.scaled_player_frame = pygame.transform.scale(self.player_frame, (self.scaled_sprite_width, self.scaled_sprite_height))
                self.scaled_player_frame = pygame.transform.flip(self.scaled_player_frame, self.flipped, False)
            else:
                self.player_attacking = False
                self.current_frame_attack = 0
        else:
            if move_x != 0:
                if self.current_frame_idle != 0:
                    self.current_frame_idle = 0
                if time.time() - self.last_update_time > self.animation_speed:
                    self.current_frame_walk = (self.current_frame_walk + 1) % self.frame_count_walk
                    self.last_update_time = time.time()
                self.frame_rect = pygame.Rect(self.current_frame_walk * self.sprite_width, 0, self.sprite_width, self.sprite_height)
                self.player_frame = self.sprite_sheet_walk.subsurface(self.frame_rect)
                self.scaled_player_frame = pygame.transform.scale(self.player_frame, (self.scaled_sprite_width, self.scaled_sprite_height))
                self.scaled_player_frame = pygame.transform.flip(self.scaled_player_frame, move_x < 0, False)
                self.flipped = move_x < 0
            else:
                if self.current_frame_walk != 0:
                    self.current_frame_walk = 0
                if time.time() - self.last_update_time > self.animation_speed:
                    self.current_frame_idle = (self.current_frame_idle + 1) % self.frame_count_idle
                    self.last_update_time = time.time()
                self.frame_rect = pygame.Rect(self.current_frame_idle * self.sprite_width, 0, self.sprite_width, self.sprite_height)
                self.player_frame = self.sprite_sheet_idle.subsurface(self.frame_rect)
                self.scaled_player_frame = pygame.transform.scale(self.player_frame, (self.scaled_sprite_width, self.scaled_sprite_height))
                self.scaled_player_frame = pygame.transform.flip(self.scaled_player_frame, self.flipped, False)

            
