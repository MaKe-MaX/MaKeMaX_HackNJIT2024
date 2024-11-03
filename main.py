import pygame
import time
import random
import math
import src.serialfr as ser
import src.Game as Game
import src.Character as Character

game = Game.Game()
player = Character.Character(r"player", 400, 0, 3)
enemy1 = Character.Character(r"enemies\leg_bot", 0, 0, 1)

# Charging bar settings
charge_level = 0           # Current charge level
max_charge = 100           # Maximum charge level
charge_speed = 1           # Speed at which the bar fills
charge_bar_width = player.sprite_width
charge_bar_height = 10     # Height of the charging bar
charge_bar_y_offset = 20   # Distance above the rectangle for the bar
charge_bar_color = Game.GREEN

# Define platforms the player can jump through from below
platforms = [pygame.Rect(300, 400, 200, 20), pygame.Rect(100, 300, 150, 20), pygame.Rect(5, 600, 800, 20)]

# Main loop
running = True
flipped = False
move_x, move_y, buttonOn, dist, distList, data = 0, 0, 0, 0, [0], []

while running:
    try:
        data = game.serial.read()  # Read joystick data
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
            
    # Character method
    player.move(platforms, move_x, move_y)
    enemy1.move(platforms, player.rect_x - enemy1.rect_x, (player.rect_y - enemy1.rect_y)*2)

    # Attack when full bar
    if charge_level == max_charge and dist <= 40:
        charge_bar_color = Game.BLUE
        if dist <= 15:
            charge_level = 0
            player.is_attacking = True
            enemy1.take_damage()
            player.attack_start_time = time.time()
            player.last_update_time = time.time()
    elif 15 <= dist <= 40:
        charge_level = min(max_charge, charge_level + charge_speed)
        charge_bar_color = Game.GREEN
    else:
        charge_level = max(0, charge_level - charge_speed)
        charge_bar_color = Game.GREEN

    if math.dist((player.rect_x,player.rect_y),(enemy1.rect_x,enemy1.rect_y)) < 30:
        if time.time() - enemy1.attack_start_time >= 3:
            enemy1.is_attacking = True
            player.take_damage()
            enemy1.attack_start_time = time.time()
            enemy1.last_update_time = time.time()

    player.change_frame(move_x, move_y)
    enemy1.change_frame(player.rect_x - enemy1.rect_x, (player.rect_y - enemy1.rect_y)*2)
    
    # Clear the screen
    game.screen.blit(game.bg, (0, 0))

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(game.screen, Game.BLACK, platform)

    # Character method: Draw the player
    game.screen.blit(player.scaled_player_frame, (player.draw_x, player.draw_y))
    game.screen.blit(enemy1.scaled_player_frame, (enemy1.draw_x, enemy1.draw_y))

    # Draw the charge bar
    if not player.is_attacking:
        charge_bar_x = player.rect_x
        charge_bar_y = player.rect_y - charge_bar_y_offset
        pygame.draw.rect(game.screen, charge_bar_color, (charge_bar_x, charge_bar_y, charge_level / max_charge * charge_bar_width, charge_bar_height))

    pygame.display.flip()

pygame.quit()