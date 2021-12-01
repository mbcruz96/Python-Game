import math
import os.path
import time
import random
from math import hypot
import pygame

import constants
from npc import Npc
from player import Player

# Pygame setup
pygame.init()
screenInfo = pygame.display.Info()
windowX = int(screenInfo.current_w * .9)
windowY = int(screenInfo.current_h * .9)
x_offset = windowX / 2
y_offset = windowY / 4
gameWindow = pygame.display.set_mode((windowX, windowY))
pygame.display.set_caption("Pygame Project")
gameClock = pygame.time.Clock()

# Pygame Images & Sound effects
backdrop = pygame.image.load(os.path.join('images', 'BLACK_BACKGROUND.png'))
game_over_screen = pygame.image.load(os.path.join('images', 'GAMEOVER.png'))
pygame.mixer.music.load(os.path.join('music', 'MainTheme.mp3'))
pygame.mixer.music.play(-1)
sword = pygame.mixer.Sound(os.path.join('soundeffects', 'sword.mp3'))
player = Player((x_offset, windowY / 2))
enemies = pygame.sprite.Group()

# Variables
running = True
x = 0
y = 0
player_direction = 0
action = 0
attack_timer = 0
vel = 10
enemy_types = {
    0: "Zombie"
}
zombie_vel = 2
zombie_range = 800
enemy_count = 4
dt = 0
damage_timer = 0
random.seed(round(time.time() * 100))
dead = False

# Tilemap & Stage variables

current_stage = constants.stages[100]
zone_code = 100
BLACK_TILE = -1
FLOOR = 0
NE_WALL = 1
NW_WALL = 2
SW_WALL = 3
SE_WALL = 4
N_WALL = 5
E_WALL = 6
S_WALL = 7
W_WALL = 8
N_CONNECTOR = 9
E_CONNECTOR = 10
S_CONNECTOR = 11
W_CONNECTOR = 12
NW_DOOR = 13
NE_DOOR = 14
tile_to_map = {
    BLACK_TILE: pygame.image.load(os.path.join('images', 'BLACK_TILE.png')).convert_alpha(),
    FLOOR: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    100: pygame.image.load(os.path.join('images', 'NW_DOOR.png')).convert_alpha(),
    101: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    102: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    103: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    104: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    105: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    106: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    107: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    108: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    109: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    110: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    111: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    112: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    NE_WALL: pygame.image.load(os.path.join('images', 'NE_WALL.png')).convert_alpha(),
    NW_WALL: pygame.image.load(os.path.join('images', 'NW_WALL.png')).convert_alpha(),
    SE_WALL: pygame.image.load(os.path.join('images', 'SE_WALL.png')).convert_alpha(),
    SW_WALL: pygame.image.load(os.path.join('images', 'SW_WALL.png')).convert_alpha(),
    N_WALL: pygame.image.load(os.path.join('images', 'N_WALL.png')).convert_alpha(),
    N_CONNECTOR: pygame.image.load(os.path.join('images', 'N_CONNECTOR.png')).convert_alpha(),
    E_WALL: pygame.image.load(os.path.join('images', 'E_WALL.png')).convert_alpha(),
    E_CONNECTOR: pygame.image.load(os.path.join('images', 'E_CONNECTOR.png')).convert_alpha(),
    S_WALL: pygame.image.load(os.path.join('images', 'S_WALL.png')).convert_alpha(),
    S_CONNECTOR: pygame.image.load(os.path.join('images', 'S_CONNECTOR.png')).convert_alpha(),
    W_WALL: pygame.image.load(os.path.join('images', 'W_WALL.png')).convert_alpha(),
    W_CONNECTOR: pygame.image.load(os.path.join('images', 'W_CONNECTOR.png')).convert_alpha(),
    NW_DOOR: pygame.image.load(os.path.join('images', 'NW_DOOR.png')).convert_alpha(),
    NE_DOOR: pygame.image.load(os.path.join('images', 'NE_DOOR.png')).convert_alpha()
}


# Creates image list
def create_map(my_map):
    generated_map = []
    for tile_row in my_map:
        internal_list = []
        for tile in tile_row:
            internal_list.append(tile_to_map[tile])
        generated_map.append(internal_list)
    return generated_map


# Finds player & enemy spawn points
def spawn():
    y_tile = 0
    x_tile = 0
    while y_tile < len(current_stage) and x_tile < len(current_stage[y_tile]) and current_stage[y_tile][x_tile] != 0:
        y_tile = random.randint(1, len(current_stage) - 1)
        x_tile = random.randint(1, len(current_stage[y_tile]) - 1)
    return int(x_offset + (x_tile - y_tile) * 64), int(y_offset + (x_tile + y_tile) * 32)


# Creates an enemy of selected type
def create_enemy():
    location = random.randint(0, 3)
    for count in range(0, constants.enemy_count[zone_code]):
        enemy_x, enemy_y = spawn()
        enemies.add(Npc((enemy_x, enemy_y), enemy_types[0]))


def draw_background():
    y_tile = 0
    for image_list in background:
        x_tile = 0
        for tile in image_list:
            if current_stage[y_tile][x_tile] == 0 or current_stage[y_tile][x_tile] > 99:
                gameWindow.blit(tile, (x_offset + (x_tile - y_tile) * 64, y_offset + (x_tile + y_tile) * 32))
            elif (y_offset + (x_tile + y_tile) * 32 - 32) <= y:
                gameWindow.blit(tile, (x_offset + (x_tile - y_tile) * 64, y_offset + (x_tile + y_tile) * 32 - 120))
            x_tile += 1
        y_tile += 1
    for background_enemy in enemies:
        if background_enemy.rect.centery < player.rect.centery:
            gameWindow.blit(background_enemy.image, background_enemy.rect)


def draw_foreground():
    y_tile = 0
    for foreground_enemy in enemies:
        if foreground_enemy.rect.centery >= player.rect.centery:
            gameWindow.blit(foreground_enemy.image, foreground_enemy.rect)
    for image_list in background:
        x_tile = 0
        for tile in image_list:
            if not (current_stage[y_tile][x_tile] == 0 or current_stage[y_tile][x_tile] > 99) and \
                    y < (y_offset + (x_tile + y_tile) * 32 - 32):
                gameWindow.blit(tile, (x_offset + (x_tile - y_tile) * 64, y_offset + (x_tile + y_tile) * 32 - 120))
            x_tile += 1
        y_tile += 1


# Handles player movement
def movement():
    player.update(position=(x, y), direction=player_direction, action=action)


def set_stage(current, next):
    global current_stage
    global zone_code
    global x
    global y
    global background
    current_stage = constants.stages[next]
    constants.cleared[zone_code] = True
    x_tile = 0
    y_tile = 0
    cur_y = 0
    for row in current_stage:
        cur_x = 0
        for tile in row:
            if tile == current:
                if cur_x == 0:
                    x_tile = cur_x + 1
                    y_tile = cur_y
                elif cur_x == len(row):
                    x_tile = cur_x - 1
                    y_tile = cur_y
                elif cur_y == 0:
                    x_tile = cur_x
                    y_tile = cur_y + 1
                else:
                    x_tile = cur_x
                    y_tile = cur_y - 1
            cur_x += 1
        cur_y += 1
    x = int(x_offset + (x_tile - y_tile) * 64)
    y = int(y_offset + (x_tile + y_tile) * 32)
    zone_code = next
    background = create_map(current_stage)
    enemies.empty()
    if not constants.cleared[zone_code]:
        create_enemy()


# Checks if player is blocked
def is_blocked(direction):
    new_x = 0
    new_y = 0
    if direction == 0:
        new_x = ((x - x_offset) / 64 + (y - y_offset) / 32) / 2
        new_y = (((y - y_offset) + (vel * 2)) / 32 - (x - x_offset) / 64) / 2
    if direction == 1:
        new_x = (((x - x_offset) - (vel * 2)) / 64 + (y - y_offset) / 32) / 2
        new_y = ((y - y_offset) / 32 - (x - x_offset) / 64) / 2
    if direction == 2:
        new_x = ((x - x_offset) / 64 + (y - y_offset) / 32) / 2
        new_y = (((y - y_offset) - (vel * 2)) / 32 - (x - x_offset) / 64) / 2
    if direction == 3:
        new_x = (((x - x_offset) + (vel * 2)) / 64 + (y - y_offset) / 32) / 2
        new_y = ((y - y_offset) / 32 - (x - x_offset) / 64) / 2
    new_y = math.ceil(new_y)
    new_x = math.floor(new_x)
    if len(enemies) < 1 and current_stage[int(new_y)][int(new_x)] > 99:
        set_stage(zone_code, current_stage[int(new_y)][int(new_x)])
        return True
    if current_stage[int(new_y)][int(new_x)] != 0:
        return True
    else:
        return False


# Handles collision detection between two rects
def collision_detection(rect1, rect2):
    if rect1.hitbox.colliderect(rect2.hitbox):
        rect1.lose_hp(rect2.damage)


# Deals damage to enemy
def deal_damage():
    for an_enemy in enemies:
        if an_enemy.hitbox.colliderect(player.hitbox.inflate(50, 50)):
            an_enemy.take_damage(player.damage)
            if an_enemy.hp < 1:
                enemies.remove(an_enemy)
                player.kill_count += 1
                player.xp += 1


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


def game_over():
    global player
    global dead
    dead = True
    set_stage(101, 100)
    for zone in constants.cleared:
        constants.cleared[zone] = False
    player = Player((x_offset, windowY / 2))
    pygame.mixer.music.unload()
    pygame.mixer.music.load(os.path.join('music', 'GameOver.mp3'))
    pygame.mixer.music.play(-1)


background = create_map(current_stage)
x, y = spawn()
# Main game loop
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not dead:
        # Handles key actions (action 2 is attack animation so they cannot act during it)
        if action != 2:
            action = 0
            if keys[pygame.K_LEFT]:
                if x > 0 and not is_blocked(1):
                    x -= vel
                player_direction = 1
                action = 1
            if keys[pygame.K_RIGHT]:
                if x < windowX and not is_blocked(3):
                    x += vel
                player_direction = 3
                action = 1
            if keys[pygame.K_UP]:
                if y > 0 and not is_blocked(2):
                    y -= vel
                player_direction = 2
                action = 1
            if keys[pygame.K_DOWN]:
                if y < windowY and not is_blocked(0):
                    y += vel
                player_direction = 0
                action = 1
            if keys[pygame.K_SPACE]:
                sword.play()
                action = 2
                deal_damage()
            attack_timer = 0
        else:
            attack_timer += dt
            if attack_timer > 500:
                attack_timer = 0
                action = 0
        gameWindow.blit(backdrop, (0, 0))
        draw_background()
        movement()
        # Performs actions on each enemy
        for enemy in enemies:
            move_enemy(enemy)
            if damage_timer > 750:
                collision_detection(player, enemy)
                damage_timer = 0
        gameWindow.blit(player.image, player.rect)
        # Draws enemies that are in front of the player, in front of the player
        draw_foreground()
    else:
        gameWindow.blit(game_over_screen, game_over_screen.get_rect(center=(windowX/2, windowY/2)))
        if keys[pygame.K_r]:
            dead = False
            pygame.mixer.music.unload()
            pygame.mixer.music.load(os.path.join('music', 'MainTheme.mp3'))
            pygame.mixer.music.play(-1)
    if player.hp < 1:
        game_over()
    pygame.display.update()
    dt = gameClock.tick(60)
    damage_timer += dt


pygame.QUIT
