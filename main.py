import pygame
import time
import os
import sys
import src.serialfr as ser
import src.Game as Game
import src.Character as Character

controller = False
try:
    ser
except:
    controller = True
game = Game.Game(controller)
player = Character.Character(r"player", 400, 0, 5)
pygame.mixer.init()
pygame.mixer.music.set_volume(0.25)
sound = pygame.mixer.Sound(os.path.join(r'assets/music', 'track1.mp3'))
sound.play()

# Charging bar settings
charge_level = 0           # Current charge level
max_charge = 100           # Maximum charge level
charge_speed = 1           # Speed at which the bar fills
charge_bar_width = player.sprite_width
charge_bar_height = 10     # Height of the charging bar
charge_bar_y_offset = 20   # Distance above the rectangle for the bar
charge_bar_color = Game.GREEN

# Main loop
running = True
flipped = False
move_x, move_y, buttonOn, dist, distList, data = 0, 0, 0, 0, [0], []

def game_over():
    # Display "Game Over" message
    font = pygame.font.Font(None, 74)  # Choose a font size
    game_over_text = font.render("Game Over", True, (255, 0, 0))  # Red color
    text_rect = game_over_text.get_rect(center=(game.screen.get_width() // 2, game.screen.get_height() // 2))
    game.screen.blit(game_over_text, text_rect)
    
    pygame.display.flip()
    pygame.time.delay(2000)  # Wait for 2 seconds

    # Optionally, ask the player if they want to restart or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


level = 1
def level_beat():
    global enemy, bg, platforms, level
    if level == 1:
        enemy = Character.Character(r"enemies\leg_bot", 0, 0, 1)
        bg = pygame.transform.scale(pygame.image.load(r"assets\backgrounds\orange_background.png"), (800, 600))
        platforms = [
            pygame.Rect(100, 450, 150, 20),  # Adjusted platform positions
            pygame.Rect(300, 350, 200, 20),
            pygame.Rect(500, 250, 150, 20),
            pygame.Rect(0, 600, 800, 20)  # Ground platform
        ]
    elif level == 2:
        enemy = Character.Character(r"enemies\chunky_bot", 0, 0, 2)
        bg = pygame.transform.scale(pygame.image.load(r"assets\backgrounds\pink_background.png"), (800, 600))
        platforms = [
            pygame.Rect(150, 450, 150, 20),
            pygame.Rect(450, 400, 200, 20),
            pygame.Rect(200, 250, 150, 20),
            pygame.Rect(0, 600, 800, 20)  # Ground platform
        ]
    elif level == 3:
        enemy = Character.Character(r"enemies\accordion_bot", 0, 0, 3)
        bg = pygame.transform.scale(pygame.image.load(r"assets\backgrounds\blue_background.png"), (800, 600))
        platforms = [
            pygame.Rect(100, 400, 200, 20),
            pygame.Rect(400, 300, 150, 20),
            pygame.Rect(250, 200, 100, 20),
            pygame.Rect(0, 600, 800, 20)  # Ground platform
    ]

    # Boss Fight Coming SOON!

    elif level == 4:
        font = pygame.font.Font(None, 74)  # Choose a font size
        game_over_text = font.render("You Win", True, (255, 0, 0))  # Red color
        text_rect = game_over_text.get_rect(center=(game.screen.get_width() // 2, game.screen.get_height() // 2))
        game.screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
        pygame.time.delay(2000)  # Wait for 2 seconds

        # Optionally, ask the player if they want to restart or quit
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
    """
        enemy = Character.Character(r"enemies\mother_bot", 0, 0, 5)
        bg = pygame.transform.scale(pygame.image.load(r"assets\backgrounds\yellow_background.png"), (800, 600))
        platforms = [pygame.Rect(300, 400, 200, 20), pygame.Rect(100, 300, 150, 20), pygame.Rect(5, 600, 800, 20)]
    """
    level += 1

level_beat()

while running:
    if controller:
        try:
            data = game.serial.read()  # Read joystick data
            move_x, move_y, buttonOn = data[0], data[1], data[2]

            # Only update `dist` if the fourth element is not zero
            if data[3] != 0:
                distList.append(data[3])
                if len(distList) > 5:
                    distList.pop(0)
                dist = sum(distList) / len(distList)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        except:
            pass
    else:
        player.movement_scale = 0.004
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()

        # Update movement variables based on keys pressed
        move_x = -500 if keys[pygame.K_LEFT] else 500 if keys[pygame.K_RIGHT] else 0
        move_y = -500 if keys[pygame.K_UP] else 500 if keys[pygame.K_DOWN] else 0
        dist = 20 if keys[pygame.K_SPACE] else 10

    # Attack when full bar
    if charge_level == max_charge and dist <= 40:
        charge_bar_color = Game.BLUE
        if dist <= 15:
            charge_level = 0
            player.is_attacking = True
            player.give_damage(enemy)
            player.attack_start_time = time.time()
            player.last_update_time = time.time()
    elif 15 <= dist <= 40:
        charge_level = min(max_charge, charge_level + charge_speed)
        charge_bar_color = Game.GREEN
    else:
        charge_level = max(0, charge_level - charge_speed)
        charge_bar_color = Game.GREEN
        
    if time.time() - enemy.attack_start_time >= 3:
        enemy.is_attacking = True
        enemy.give_damage(player)
        enemy.attack_start_time = time.time()
        enemy.last_update_time = time.time()

    if player.update(platforms, move_x, move_y):
        game_over()
    if enemy.update(platforms, player.rect_x - enemy.rect_x, (player.rect_y - enemy.rect_y)*2):
        level_beat()
    
    # Clear the screen
    game.screen.blit(bg, (0, 0))

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(game.screen, Game.BLACK, platform)

    # Character method: Draw the player
    game.screen.blit(player.scaled_player_frame, (player.draw_x, player.draw_y))
    game.screen.blit(enemy.scaled_player_frame, (enemy.draw_x, enemy.draw_y))

    # Draw the charge bar
    if not player.is_attacking:
        charge_bar_x = player.rect_x
        charge_bar_y = player.rect_y - charge_bar_y_offset
        pygame.draw.rect(game.screen, charge_bar_color, (charge_bar_x, charge_bar_y, charge_level / max_charge * charge_bar_width, charge_bar_height))

    pygame.display.flip()

pygame.quit()