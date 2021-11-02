import math
import os.path
import time
import random
from math import hypot
import pygame

from npc import Npc
from player import Player

# Pygame setup
pygame.init()
windowX = 1680
windowY = 1050
gameWindow = pygame.display.set_mode((windowX, windowY))
pygame.display.set_caption("Pygame Project")
gameClock = pygame.time.Clock()

# Pygame Images & Sound effects
pygame.mixer.music.load(os.path.join('music', 'dark.mp3'))
pygame.mixer.music.play(-1)
background = pygame.image.load(os.path.join('images', 'placeholdermap.jpg')).convert_alpha()
sword = pygame.mixer.Sound(os.path.join('soundeffects', 'sword.mp3'))
player = Player((windowX / 2, windowY / 2))
enemies = pygame.sprite.Group()

# Variables
running = True
x = 0
y = 0
player_direction = 0
action = 0
attack_timer = 0
vel = 3
enemy_types = {
    0: "Zombie"
}
zombie_vel = 2
zombie_range = 800
enemy_count = 4
dt = 0
damage_timer = 0
random.seed(round(time.time() * 100))


# Creates an enemy of selected type
def create_enemy():
    location = random.randint(0, 3)
    if location == 0:
        enemies.add(Npc((random.randint(0, windowX), 0), enemy_types[0]))
    elif location == 1:
        enemies.add(Npc((random.randint(0, windowX), windowY), enemy_types[0]))
    elif location == 2:
        enemies.add(Npc((0, random.randint(0, windowY)), enemy_types[0]))
    elif location == 3:
        enemies.add(Npc((windowX, random.randint(0, windowY)), enemy_types[0]))


# Handles player movement
def movement():
    player.update(position=(x, y), direction=player_direction, action=action)


# Checks if player is blocked
def is_blocked(entity):
    return False


# Handles collision detection between two rects
def collision_detection(rect1, rect2):
    if rect1.rect.colliderect(rect2.rect):
        print("took damage")
        rect1.lose_hp(rect2.damage)


# Handles enemy movement
def move_enemy(the_enemy):
    if hypot(the_enemy.rect.centerx - player.rect.centerx,
             the_enemy.rect.centery - player.rect.centery) < zombie_range:
        dx = the_enemy.rect.centerx - player.rect.centerx
        dy = the_enemy.rect.centery - player.rect.centery
        theta = math.atan2(dy, dx)
        dx_direction = -1
        if dx == -1:
            dx_direction = 1
        dy_direction = -1
        if dy == -1:
            dy_direction = 1
        if abs(dx) > abs(dy):
            if dx > 0:
                the_enemy.update((the_enemy.rect.centerx + math.cos(theta) * zombie_vel * dx_direction,
                                  the_enemy.rect.centery + math.sin(theta) * zombie_vel * dy_direction), direction=1)
            else:
                the_enemy.update((the_enemy.rect.centerx + math.cos(theta) * zombie_vel * dx_direction,
                                  the_enemy.rect.centery + math.sin(theta) * zombie_vel * dy_direction), direction=3)
        else:
            if dy > 0:
                the_enemy.update((the_enemy.rect.centerx + math.cos(theta) * zombie_vel * dx_direction,
                                  the_enemy.rect.centery + math.sin(theta) * zombie_vel * dy_direction), direction=2)
            else:
                the_enemy.update((the_enemy.rect.centerx + math.cos(theta) * zombie_vel * dx_direction,
                                  the_enemy.rect.centery + math.sin(theta) * zombie_vel * dy_direction), direction=0)


# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    # Handles key actions (action 2 is attack animation so they cannot act during it)
    if action != 2:
        action = 0
        if keys[pygame.K_LEFT]:
            if x > 0 and not is_blocked(player):
                x -= vel
            player_direction = 1
            action = 1
        if keys[pygame.K_RIGHT]:
            if x < windowX and not is_blocked(player):
                x += vel
            player_direction = 3
            action = 1
        if keys[pygame.K_UP]:
            if y > 0 and not is_blocked(player):
                y -= vel
            player_direction = 2
            action = 1
        if keys[pygame.K_DOWN]:
            if y < windowY and not is_blocked(player):
                y += vel
            player_direction = 0
            action = 1
        if keys[pygame.K_SPACE]:
            sword.play()
            action = 2
        attack_timer = 0
    else:
        attack_timer += dt
        if attack_timer > 500:
            attack_timer = 0
            action = 0
    gameWindow.blit(background, (0, 0))
    movement()
    if enemy_count > len(enemies):
        create_enemy()
    # Performs actions on each enemy
    for enemy in enemies:
        move_enemy(enemy)
        if damage_timer > 750:
            collision_detection(player, enemy)
            damage_timer = 0
        if enemy.rect.centery < player.rect.centery:
            gameWindow.blit(enemy.image, enemy.rect)
    gameWindow.blit(player.image, player.rect)
    # Draws enemies that are in front of the player, in front of the player
    for enemy in enemies:
        if enemy.rect.centery >= player.rect.centery:
            gameWindow.blit(enemy.image, enemy.rect)
    pygame.display.update()
    dt = gameClock.tick(60)
    damage_timer += dt

pygame.QUIT
