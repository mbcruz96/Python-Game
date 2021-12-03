import math
import os.path
import time
import random
from math import hypot
import pygame

import constants
import database
from npc import Npc
from player import Player

# Pygame setup
pygame.init()
screenInfo = pygame.display.Info()
windowX = int(screenInfo.current_w * .9)
windowY = int(screenInfo.current_h * .9)
x_offset = windowX / 2
y_offset = windowY / 8
gameWindow = pygame.display.set_mode((windowX, windowY))
pygame.display.set_caption("Pygame Project")
gameClock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

# Pygame Images & Sound effects
backdrop = pygame.image.load(os.path.join('images', 'BLACK_BACKGROUND.png'))
game_over_screen = pygame.image.load(os.path.join('images', 'GAMEOVER.png'))
menu_screen = pygame.image.load(os.path.join('images', 'MENU.png'))
victory_screen = pygame.image.load(os.path.join('images', 'VICTORY.png'))
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
vel = 8
zombie_vel = 2
e_range = 800
enemy_count = 4
dt = 0
damage_timer = 0
random.seed(round(time.time() * 100))
dead = False
player_victory = False
in_menu = True

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
    113: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    114: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    115: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    116: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    117: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    118: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    119: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
    120: pygame.image.load(os.path.join('images', 'FLOOR.png')).convert_alpha(),
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
    for count in range(0, constants.enemy_count[zone_code]):
        enemy_x, enemy_y = spawn()
        enemies.add(Npc((enemy_x, enemy_y), constants.enemy_types[zone_code]))


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


# Creates the current stage and populates it
def set_stage(current, next):
    global current_stage
    global zone_code
    global x
    global y
    global background
    global zombie_vel
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
    zombie_vel = constants.enemy_vel[zone_code]
    if not constants.cleared[zone_code]:
        create_enemy()
    if zone_code == 120:
        for boss in enemies:
            boss.hp = 100
        pygame.mixer.music.unload()
        pygame.mixer.music.load(os.path.join('music', 'FinalBoss.mp3'))
        pygame.mixer.music.play(-1)


# Checks if player is blocked
def is_blocked(cur_x, cur_y, direction):
    new_x = 0
    new_y = 0
    if direction == 0:
        new_x = ((cur_x - x_offset) / 64 + (cur_y - y_offset) / 32) / 2
        new_y = (((cur_y - y_offset) + (vel * 2)) / 32 - (cur_x - x_offset) / 64) / 2
    if direction == 2:
        new_x = (((cur_x - x_offset) - (vel * 2)) / 64 + (cur_y - y_offset) / 32) / 2
        new_y = ((cur_y - y_offset) / 32 - (cur_x - x_offset) / 64) / 2
    if direction == 4:
        new_x = ((cur_x - x_offset) / 64 + (cur_y - y_offset) / 32) / 2
        new_y = (((cur_y - y_offset) - (vel * 2)) / 32 - (cur_x - x_offset) / 64) / 2
    if direction == 6:
        new_x = (((cur_x - x_offset) + (vel * 2)) / 64 + (cur_y - y_offset) / 32) / 2
        new_y = ((cur_y - y_offset) / 32 - (cur_x - x_offset) / 64) / 2
    if direction == 1:
        new_x = (((cur_x - x_offset) - (hypot(vel) * 3)) / 64 + (cur_y - y_offset) / 32) / 2
        new_y = (((cur_y - y_offset) + (hypot(vel) * 3)) / 32 - (cur_x - x_offset) / 64) / 2
    if direction == 3:
        new_x = (((cur_x - x_offset) - (hypot(vel) * 3)) / 64 + (cur_y - y_offset) / 32) / 2
        new_y = (((cur_y - y_offset) - (hypot(vel) * 3)) / 32 - (cur_x - x_offset) / 64) / 2
    if direction == 5:
        new_x = (((cur_x - x_offset) + (hypot(vel) * 3)) / 64 + (cur_y - y_offset) / 32) / 2
        new_y = (((cur_y - y_offset) - (hypot(vel) * 3)) / 32 - (cur_x - x_offset) / 64) / 2
    if direction == 7:
        new_x = (((cur_x - x_offset) + (hypot(vel) * 3)) / 64 + (cur_y - y_offset) / 32) / 2
        new_y = (((cur_y - y_offset) + (hypot(vel) * 3)) / 32 - (cur_x - x_offset) / 64) / 2
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
    global vel
    hits = 0
    max_hits = int(player.level / 2)
    for an_enemy in enemies:
        hits += 1
        if player.damage_box.colliderect(an_enemy.hitbox):
            an_enemy.take_damage(player.damage)
            sword.play()
            if an_enemy.hp < 1:
                enemies.remove(an_enemy)
                player.kill_count += 1
                player.xp += 1
                player.xp_to_level()
                vel = player.level + 7
                if zone_code == 120:
                    constants.cleared[zone_code] = True
            if hits > max_hits:
                break


# Handles enemy movement
def move_enemy(the_enemy):
    dx = the_enemy.rect.centerx - player.rect.centerx
    dy = the_enemy.rect.centery - player.rect.centery
    theta = math.atan2(dy, dx)
    if -5 * math.pi / 6 <= theta <= -2 * math.pi / 3:
        enemy_direction = 7
    elif -2 * math.pi / 3 <= theta <= -math.pi / 3:
        enemy_direction = 0
    elif -math.pi / 3 <= theta <= -math.pi / 6:
        enemy_direction = 1
    elif -math.pi / 6 <= theta <= math.pi / 6:
        enemy_direction = 2
    elif math.pi / 6 <= theta <= math.pi / 3:
        enemy_direction = 3
    elif math.pi / 3 <= theta <= 2 * math.pi / 3:
        enemy_direction = 4
    elif 2 * math.pi / 3 <= theta <= 5 * math.pi / 6:
        enemy_direction = 5
    else:
        enemy_direction = 6
    if the_enemy.hitbox.colliderect(player.hitbox):
        the_enemy.update((the_enemy.rect.centerx, the_enemy.rect.centery), direction=enemy_direction, action=2)
    elif not is_blocked(the_enemy.rect.centerx, the_enemy.rect.centery, enemy_direction) and hypot(dx, dy) < e_range:
        dx_direction = -1
        if dx == -1:
            dx_direction = 1
        dy_direction = -1
        if dy == -1:
            dy_direction = 1
        if abs(dx) > abs(dy):
            if dx > 0:
                the_enemy.update((the_enemy.rect.centerx + math.cos(theta) * zombie_vel * dx_direction,
                                  the_enemy.rect.centery + math.sin(theta) * zombie_vel * dy_direction),
                                 direction=enemy_direction)
            else:
                the_enemy.update((the_enemy.rect.centerx + math.cos(theta) * zombie_vel * dx_direction,
                                  the_enemy.rect.centery + math.sin(theta) * zombie_vel * dy_direction),
                                 direction=enemy_direction)
        else:
            if dy > 0:
                the_enemy.update((the_enemy.rect.centerx + math.cos(theta) * zombie_vel * dx_direction,
                                  the_enemy.rect.centery + math.sin(theta) * zombie_vel * dy_direction),
                                 direction=enemy_direction)
            else:
                the_enemy.update((the_enemy.rect.centerx + math.cos(theta) * zombie_vel * dx_direction,
                                  the_enemy.rect.centery + math.sin(theta) * zombie_vel * dy_direction),
                                 direction=enemy_direction)


def victory():
    global clear_time
    database.save_scores(player.kill_count, player.level, clear_time/1000)
    pygame.mixer.music.unload()
    pygame.mixer.music.load(os.path.join('music', 'Victory.mp3'))
    pygame.mixer.music.play(-1)


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
clear_time = 0
pygame.mixer.music.load(os.path.join('music', 'Menu.mp3'))
pygame.mixer.music.play(-1)
# Main game loop
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if in_menu:
        gameWindow.blit(menu_screen, menu_screen.get_rect(center=(windowX / 2, windowY / 2)))
        if keys[pygame.K_1]:
            in_menu = False
            clear_time = 0
            pygame.mixer.music.unload()
            pygame.mixer.music.load(os.path.join('music', 'MainTheme.mp3'))
            pygame.mixer.music.play(-1)
        elif keys[pygame.K_2]:
            gameWindow.blit(backdrop, (0, 0))
            score_list = database.load_scores()
            highscores = []
            i = 1
            for score in score_list:
                highscores.append(font.render(str(i) + ") Kills: " + str(score[0]) + " Level: " + str(score[1]) +
                                              " Seconds: " + str(score[2]),
                                              True, (255, 255, 255), (0, 0, 0)))
                i += 1
            y_score = 1
            for score in highscores:
                gameWindow.blit(score, score.get_rect(center=(windowX / 2, y_score * windowY / 11)))
                y_score += 1
        elif keys[pygame.K_ESCAPE]:
            running = False
    elif not player_victory and constants.cleared[120]:
        player_victory = True
        playerText = font.render("Your Final Stats: " +
                                 "Level: " + str(player.level) + " Kills: " + str(player.kill_count) +
                                 " Time (Seconds): " + str(clear_time / 1000),
                                 True, (255, 255, 255), (0, 0, 0))
        gameWindow.blit(victory_screen, victory_screen.get_rect(center=(windowX / 2, windowY / 2)))
        gameWindow.blit(playerText, playerText.get_rect(center=(windowX / 2, 4 * windowY / 5)))
        victory()
        clear_time = 0
    elif player_victory:
        if keys[pygame.K_r]:
            dead = False
            clear_time = 0
            player_victory = False
            set_stage(101, 100)
            for zone in constants.cleared:
                constants.cleared[zone] = False
            player = Player((x_offset, windowY / 2))
            pygame.mixer.music.unload()
            pygame.mixer.music.load(os.path.join('music', 'MainTheme.mp3'))
            pygame.mixer.music.play(-1)
        elif keys[pygame.K_m]:
            dead = False
            player_victory = False
            set_stage(101, 100)
            for zone in constants.cleared:
                constants.cleared[zone] = False
            player = Player((x_offset, windowY / 2))
            in_menu = True
            pygame.mixer.music.unload()
            pygame.mixer.music.load(os.path.join('music', 'Menu.mp3'))
            pygame.mixer.music.play(-1)
    elif not dead:
        # Handles key actions (action 2 is attack animation so they cannot act during it)
        if action != 2:
            action = 0
            if keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
                player_direction = 1
                if not is_blocked(x, y, player_direction) or keys[pygame.K_LSHIFT]:
                    x -= hypot(vel)
                    y += hypot(vel)
                    action = 1
            elif keys[pygame.K_LEFT] and keys[pygame.K_UP]:
                player_direction = 3
                if not is_blocked(x, y, player_direction) or keys[pygame.K_LSHIFT]:
                    x -= hypot(vel)
                    y -= hypot(vel)
                    action = 1
            elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
                player_direction = 5
                if not is_blocked(x, y, player_direction) or keys[pygame.K_LSHIFT]:
                    x += hypot(vel)
                    y -= hypot(vel)
                    action = 1
            elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
                player_direction = 7
                if not is_blocked(x, y, player_direction) or keys[pygame.K_LSHIFT]:
                    x += hypot(vel)
                    y += hypot(vel)
                    action = 1
            else:
                if keys[pygame.K_LEFT]:
                    player_direction = 2
                    if not is_blocked(x, y, player_direction) or keys[pygame.K_LSHIFT]:
                        x -= vel
                    action = 1
                if keys[pygame.K_RIGHT]:
                    player_direction = 6
                    if not is_blocked(x, y, player_direction) or keys[pygame.K_LSHIFT]:
                        x += vel
                    action = 1
                if keys[pygame.K_UP]:
                    player_direction = 4
                    if not is_blocked(x, y, player_direction) or keys[pygame.K_LSHIFT]:
                        y -= vel
                    action = 1
                if keys[pygame.K_DOWN]:
                    player_direction = 0
                    if not is_blocked(x, y, player_direction) or keys[pygame.K_LSHIFT]:
                        y += vel
                    action = 1
            if keys[pygame.K_SPACE]:
                action = 2
                deal_damage()
            attack_timer = 0
        else:
            attack_timer += dt
            if attack_timer > 250:
                attack_timer = 0
                action = 0
        gameWindow.blit(backdrop, (0, 0))
        draw_background()
        movement()
        # Performs actions on each enemy
        for enemy in enemies:
            move_enemy(enemy)
            if damage_timer > 500:
                collision_detection(player, enemy)
                damage_timer = 0
        gameWindow.blit(player.image, player.rect)
        # Draws enemies that are in front of the player, in front of the player
        draw_foreground()
    else:
        gameWindow.blit(game_over_screen, game_over_screen.get_rect(center=(windowX / 2, windowY / 2)))
        if keys[pygame.K_r]:
            dead = False
            clear_time = 0
            pygame.mixer.music.unload()
            pygame.mixer.music.load(os.path.join('music', 'MainTheme.mp3'))
            pygame.mixer.music.play(-1)
        elif keys[pygame.K_m]:
            dead = False
            in_menu = True
            pygame.mixer.music.unload()
            pygame.mixer.music.load(os.path.join('music', 'Menu.mp3'))
            pygame.mixer.music.play(-1)
    if player.hp < 1:
        game_over()
    playerText = font.render("HP: " + str(player.hp) + " Lvl: " + str(player.level) + " XP: " + str(player.xp) +
                             " Damage: " + str(player.damage) + " Kill Count: " + str(player.kill_count) +
                             " Armor: " + str(player.armor), True, (255, 255, 255), (0, 0, 0))
    if not dead and not in_menu and not player_victory:
        gameWindow.blit(playerText, (0, 0))
    pygame.display.update()
    dt = gameClock.tick(30)
    clear_time += dt
    damage_timer += dt

pygame.QUIT
