import pygame
import time

gravity = 0.1  # Gravity force pulling the rectangle down

class Character:
    def __init__(self, name, x, y, lives):
        # Load sprite sheets
        self.sprite_sheet_walk = pygame.image.load(rf"assets\{name}\walk.png").convert_alpha()
        self.sprite_sheet_idle = pygame.image.load(rf"assets\{name}\idle.png").convert_alpha()
        self.sprite_sheet_hit = pygame.image.load(rf"assets\{name}\whitehit.png").convert_alpha()
        self.sprite_sheet_death = pygame.image.load(rf"assets\{name}\death.png").convert_alpha()
        try:
            self.sprite_sheet_attack = pygame.image.load(rf"assets\{name}\attack.png").convert_alpha()
        except:
            self.sprite_sheet_birth = pygame.image.load(rf"assets\{name}\birth.png").convert_alpha()
            self.sprite_sheet_bomb = pygame.image.load(rf"assets\{name}\bomb.png").convert_alpha()

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
        self.frame_count_death = self.sprite_sheet_death.get_width() // self.sprite_width  # Number of frames in the death sprite sheet
        self.current_frame_walk = 0  # Track the current frame for walking
        self.current_frame_idle = 0   # Track the current frame for idle
        self.current_frame_attack = 0   # Track the current frame for attack
        self.current_frame_death = 0   # Track the current frame for death
        self.current_frame_hit = 0   # Track the current frame for hit
        self.current_frame = 0
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
        self.rect_x = x  # Fixed horizontal position
        self.rect_y = y  # Starting vertical position
        self.movement_scale = 0.006  # Adjust this to scale movement to the screen size
        self.draw_x = self.rect_x + (self.sprite_width - self.scaled_sprite_width) // 2
        self.draw_y = self.rect_y + (self.sprite_height - self.scaled_sprite_height) // 2
        self.lives = lives
        self.dead = False

        # Attack and hit states
        self.is_attacking = False
        self.is_hit = False
        self.attack_frame_duration = 0.5
        self.hit_frame_duration = 0.5
        self.attack_start_time = 0
        self.hit_start_time = 0

        # Death states
        self.is_dead = False
        self.death_frame_duration = 0.5
        self.death_start_time = 0

    def take_damage(self):
        if not self.is_dead and not self.is_hit:
            self.lives -= 1
            self.is_hit = True
            self.hit_start_time = time.time()
            if self.lives <= 0:
                self.is_dead = True
                self.death_start_time = time.time()

    def move(self, platforms, move_x, move_y):
        # Horizontal movement
        self.rect_x = min(800 - 3 * self.sprite_width / 4 - 6, max(-self.sprite_width / 4 + 6, self.rect_x + move_x * self.movement_scale))

        # Jump mechanics
        if not self.is_jumping and move_y < -480:
            self.is_jumping = True
            self.vertical_velocity = -self.jump_velocity

        # Apply gravity if jumping
        if self.is_jumping:
            self.rect_y += self.vertical_velocity
            self.vertical_velocity += gravity

        # Platform collision detection
        on_platform = False

        for platform in platforms:
            if self.vertical_velocity > 0 and self.rect_y + self.sprite_height <= platform.top and self.rect_y + self.sprite_height + self.vertical_velocity >= platform.top:
                if self.rect_x + 3 * self.sprite_width / 4.5 > platform.left and self.rect_x + self.sprite_width / 3.5 < platform.right:
                    self.rect_y = platform.top - self.sprite_height
                    self.vertical_velocity = 0
                    self.is_jumping = False
                    on_platform = True
                    break

        if not on_platform:
            self.is_jumping = True

        self.draw_x = self.rect_x + (self.sprite_width - self.scaled_sprite_width) // 2
        self.draw_y = self.rect_y + (self.sprite_height - self.scaled_sprite_height) // 2

    def change_frame(self, move_x, move_y):
        # Player Character: Animation logic (walking, idle, attack, hit, death)
        if self.is_dead:
            if time.time() - self.death_start_time < self.death_frame_duration:
                if time.time() - self.last_update_time > self.animation_speed:
                    self.current_frame_death = (self.current_frame_death + 1) % self.frame_count_death
                    self.current_frame = self.current_frame_death
                    self.last_update_time = time.time()
                self.frame_rect = pygame.Rect(min(self.current_frame * self.sprite_width, self.sprite_sheet_death.get_width() - self.sprite_width), 0, self.sprite_width, self.sprite_height)
                self.player_frame = self.sprite_sheet_death.subsurface(self.frame_rect)
                self.scaled_player_frame = pygame.transform.scale(self.player_frame, (self.scaled_sprite_width, self.scaled_sprite_height))
        elif self.is_hit:
            if time.time() - self.hit_start_time < self.hit_frame_duration:
                if time.time() - self.last_update_time > self.animation_speed:
                    self.current_frame_hit = (self.current_frame_hit + 1) % self.frame_count_idle
                    self.current_frame = self.current_frame_hit
                    self.last_update_time = time.time()
                self.frame_rect = pygame.Rect(min(self.current_frame * self.sprite_width, self.sprite_sheet_hit.get_width() - self.sprite_width), 0, self.sprite_width, self.sprite_height)
                self.player_frame = self.sprite_sheet_hit.subsurface(self.frame_rect)
                self.scaled_player_frame = pygame.transform.scale(self.player_frame, (self.scaled_sprite_width, self.scaled_sprite_height))
            else:
                self.is_hit = False
                self.current_frame_hit = 0
                self.current_frame = self.current_frame_hit

        elif self.is_attacking:
            if time.time() - self.attack_start_time < self.attack_frame_duration:
                if time.time() - self.last_update_time > self.animation_speed:
                    self.current_frame_attack = (self.current_frame_attack + 1) % self.frame_count_attack
                    self.current_frame = self.current_frame_attack
                    self.last_update_time = time.time()
                self.frame_rect = pygame.Rect(min(self.current_frame * self.sprite_width, self.sprite_sheet_attack.get_width() - self.sprite_width), 0, self.sprite_width, self.sprite_height)
                self.player_frame = self.sprite_sheet_attack.subsurface(self.frame_rect)
                self.scaled_player_frame = pygame.transform.scale(self.player_frame, (self.scaled_sprite_width, self.scaled_sprite_height))
                self.scaled_player_frame = pygame.transform.flip(self.scaled_player_frame, self.flipped, False)
            else:
                self.is_attacking = False
                self.current_frame_attack = 0
                self.current_frame = self.current_frame_attack
        else:
            if move_x != 0:
                if self.current_frame_idle != 0:
                    self.current_frame_idle = 0
                if time.time() - self.last_update_time > self.animation_speed:
                    self.current_frame_walk = (self.current_frame_walk + 1) % self.frame_count_walk
                    self.current_frame = self.current_frame_walk
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
                    self.current_frame = self.current_frame_idle
                    self.last_update_time = time.time()
                self.frame_rect = pygame.Rect(self.current_frame_idle * self.sprite_width, 0, self.sprite_width, self.sprite_height)
                self.player_frame = self.sprite_sheet_idle.subsurface(self.frame_rect)
                self.scaled_player_frame = pygame.transform.scale(self.player_frame, (self.scaled_sprite_width, self.scaled_sprite_height))
                self.scaled_player_frame = pygame.transform.flip(self.scaled_player_frame, self.flipped, False)
            
