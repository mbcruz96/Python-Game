import math
import os

import pygame as pygame

import spriteloader


class Player(pygame.sprite.Sprite):

    def __init__(self, position):
        super().__init__()
        self.damage = 5
        self.hp = 100
        self.armor = 0
        self.xp = 0
        self.kill_count = 0
        self.level = 1
        self.level5 = False
        self.level10 = False
        player_sprites = spriteloader.spritesheet(os.path.join('images', 'lvl1player.png'))
        self.last_action = 0
        self.animation_speed = 1
        self.animation_timing = 0
        self.player_movement = []
        self.player_move_sprite_north = []
        self.player_move_sprite_south = []
        self.player_move_sprite_west = []
        self.player_move_sprite_east = []
        self.player_move_sprite_northwest = []
        self.player_move_sprite_northeast = []
        self.player_move_sprite_southeast = []
        self.player_move_sprite_southwest = []
        self.player_attack = []
        self.player_attack_sprite_north = []
        self.player_attack_sprite_south = []
        self.player_attack_sprite_west = []
        self.player_attack_sprite_east = []
        self.player_attack_sprite_northwest = []
        self.player_attack_sprite_northeast = []
        self.player_attack_sprite_southeast = []
        self.player_attack_sprite_southwest = []
        self.player_idle = []
        self.player_idle.append(player_sprites.image_at((20, 783, 76, 95), colorkey=(255, 255, 255)))
        self.player_idle.append(player_sprites.image_at((20, 911, 76, 95), colorkey=(255, 255, 255)))
        self.player_idle.append(player_sprites.image_at((20, 15, 76, 95), colorkey=(255, 255, 255)))
        self.player_idle.append(player_sprites.image_at((20, 143, 76, 95), colorkey=(255, 255, 255)))
        self.player_idle.append(player_sprites.image_at((20, 271, 76, 95), colorkey=(255, 255, 255)))
        self.player_idle.append(player_sprites.image_at((20, 399, 76, 95), colorkey=(255, 255, 255)))
        self.player_idle.append(player_sprites.image_at((20, 527, 76, 95), colorkey=(255, 255, 255)))
        self.player_idle.append(player_sprites.image_at((20, 655, 76, 95), colorkey=(255, 255, 255)))
        for x in range(512, 1536, 128):
            self.player_move_sprite_west.append(player_sprites.image_at((x + 20, 15, 76, 95), colorkey=(255, 255, 255)))
            self.player_move_sprite_east.append(player_sprites.image_at((x + 20, 527, 76, 95), colorkey=(255, 255, 255)))
            self.player_move_sprite_south.append(player_sprites.image_at((x + 20, 783, 76, 95), colorkey=(255, 255, 255)))
            self.player_move_sprite_north.append(player_sprites.image_at((x + 20, 271, 76, 95), colorkey=(255, 255, 255)))
            self.player_move_sprite_northeast.append(player_sprites.image_at((x + 20, 399, 76, 95), colorkey=(255, 255, 255)))
            self.player_move_sprite_northwest.append(player_sprites.image_at((x + 20, 143, 76, 95), colorkey=(255, 255, 255)))
            self.player_move_sprite_southeast.append(player_sprites.image_at((x + 20, 655, 76, 95), colorkey=(255, 255, 255)))
            self.player_move_sprite_southwest.append(player_sprites.image_at((x + 20, 911, 76, 95), colorkey=(255, 255, 255)))
        self.player_movement.append(self.player_move_sprite_south)
        self.player_movement.append(self.player_move_sprite_southwest)
        self.player_movement.append(self.player_move_sprite_west)
        self.player_movement.append(self.player_move_sprite_northwest)
        self.player_movement.append(self.player_move_sprite_north)
        self.player_movement.append(self.player_move_sprite_northeast)
        self.player_movement.append(self.player_move_sprite_east)
        self.player_movement.append(self.player_move_sprite_southeast)
        for x in range(1536, 2048, 128):
            self.player_attack_sprite_west.append(player_sprites.image_at((x + 20, 15, 76, 95), colorkey=(255, 255, 255)))
            self.player_attack_sprite_east.append(player_sprites.image_at((x + 20, 527, 76, 95), colorkey=(255, 255, 255)))
            self.player_attack_sprite_south.append(player_sprites.image_at((x + 20, 783, 76, 95), colorkey=(255, 255, 255)))
            self.player_attack_sprite_north.append(player_sprites.image_at((x + 20, 271, 76, 95), colorkey=(255, 255, 255)))
            self.player_attack_sprite_northeast.append(player_sprites.image_at((x + 20, 399, 76, 95), colorkey=(255, 255, 255)))
            self.player_attack_sprite_northwest.append(player_sprites.image_at((x + 20, 143, 76, 95), colorkey=(255, 255, 255)))
            self.player_attack_sprite_southeast.append(player_sprites.image_at((x + 20, 655, 76, 95), colorkey=(255, 255, 255)))
            self.player_attack_sprite_southwest.append(player_sprites.image_at((x + 20, 911, 76, 95), colorkey=(255, 255, 255)))
        self.player_attack.append(self.player_attack_sprite_south)
        self.player_attack.append(self.player_attack_sprite_southwest)
        self.player_attack.append(self.player_attack_sprite_west)
        self.player_attack.append(self.player_attack_sprite_northwest)
        self.player_attack.append(self.player_attack_sprite_north)
        self.player_attack.append(self.player_attack_sprite_northeast)
        self.player_attack.append(self.player_attack_sprite_east)
        self.player_attack.append(self.player_attack_sprite_southeast)
        self.current_sprite = 0
        self.image = self.player_move_sprite_south[self.current_sprite]
        self.rect = self.image.get_rect(center=position)
        self.hitbox = self.rect.inflate(-46, -26)
        self.damage_box = self.rect.inflate(20, 20).move(0, 20)

    def lose_hp(self, damage):
        damage_taken = damage - self.armor
        if damage_taken > 0:
            self.hp = self.hp - damage_taken

    def xp_to_level(self):
        self.damage = 5 + int(math.sqrt(self.xp)) * 2
        self.armor = 0 + int(math.sqrt(self.xp)) * 2
        self.level = int(math.sqrt(self.xp) + 1)
        if not self.level5 and self.xp >= 16:
            self.level5 = True
            self.hp += 10
            player_sprites = spriteloader.spritesheet(os.path.join('images', 'lvl5player.png'))
            self.player_movement = []
            self.player_move_sprite_north = []
            self.player_move_sprite_south = []
            self.player_move_sprite_west = []
            self.player_move_sprite_east = []
            self.player_move_sprite_northwest = []
            self.player_move_sprite_northeast = []
            self.player_move_sprite_southeast = []
            self.player_move_sprite_southwest = []
            self.player_attack = []
            self.player_attack_sprite_north = []
            self.player_attack_sprite_south = []
            self.player_attack_sprite_west = []
            self.player_attack_sprite_east = []
            self.player_attack_sprite_northwest = []
            self.player_attack_sprite_northeast = []
            self.player_attack_sprite_southeast = []
            self.player_attack_sprite_southwest = []
            self.player_idle = []
            self.player_idle.append(player_sprites.image_at((20, 783, 76, 95), colorkey=(255, 255, 255)))
            self.player_idle.append(player_sprites.image_at((20, 911, 76, 95), colorkey=(255, 255, 255)))
            self.player_idle.append(player_sprites.image_at((20, 15, 76, 95), colorkey=(255, 255, 255)))
            self.player_idle.append(player_sprites.image_at((20, 143, 76, 95), colorkey=(255, 255, 255)))
            self.player_idle.append(player_sprites.image_at((20, 271, 76, 95), colorkey=(255, 255, 255)))
            self.player_idle.append(player_sprites.image_at((20, 399, 76, 95), colorkey=(255, 255, 255)))
            self.player_idle.append(player_sprites.image_at((20, 527, 76, 95), colorkey=(255, 255, 255)))
            self.player_idle.append(player_sprites.image_at((20, 655, 76, 95), colorkey=(255, 255, 255)))
            for x in range(512, 1536, 128):
                self.player_move_sprite_west.append(
                    player_sprites.image_at((x + 20, 15, 76, 95), colorkey=(255, 255, 255)))
                self.player_move_sprite_east.append(
                    player_sprites.image_at((x + 20, 527, 76, 95), colorkey=(255, 255, 255)))
                self.player_move_sprite_south.append(
                    player_sprites.image_at((x + 20, 783, 76, 95), colorkey=(255, 255, 255)))
                self.player_move_sprite_north.append(
                    player_sprites.image_at((x + 20, 271, 76, 95), colorkey=(255, 255, 255)))
                self.player_move_sprite_northeast.append(
                    player_sprites.image_at((x + 20, 399, 76, 95), colorkey=(255, 255, 255)))
                self.player_move_sprite_northwest.append(
                    player_sprites.image_at((x + 20, 143, 76, 95), colorkey=(255, 255, 255)))
                self.player_move_sprite_southeast.append(
                    player_sprites.image_at((x + 20, 655, 76, 95), colorkey=(255, 255, 255)))
                self.player_move_sprite_southwest.append(
                    player_sprites.image_at((x + 20, 911, 76, 95), colorkey=(255, 255, 255)))
            self.player_movement.append(self.player_move_sprite_south)
            self.player_movement.append(self.player_move_sprite_southwest)
            self.player_movement.append(self.player_move_sprite_west)
            self.player_movement.append(self.player_move_sprite_northwest)
            self.player_movement.append(self.player_move_sprite_north)
            self.player_movement.append(self.player_move_sprite_northeast)
            self.player_movement.append(self.player_move_sprite_east)
            self.player_movement.append(self.player_move_sprite_southeast)
            for x in range(1536, 2048, 128):
                self.player_attack_sprite_west.append(
                    player_sprites.image_at((x + 20, 15, 76, 95), colorkey=(255, 255, 255)))
                self.player_attack_sprite_east.append(
                    player_sprites.image_at((x + 20, 527, 76, 95), colorkey=(255, 255, 255)))
                self.player_attack_sprite_south.append(
                    player_sprites.image_at((x + 20, 783, 76, 95), colorkey=(255, 255, 255)))
                self.player_attack_sprite_north.append(
                    player_sprites.image_at((x + 20, 271, 76, 95), colorkey=(255, 255, 255)))
                self.player_attack_sprite_northeast.append(
                    player_sprites.image_at((x + 20, 399, 76, 95), colorkey=(255, 255, 255)))
                self.player_attack_sprite_northwest.append(
                    player_sprites.image_at((x + 20, 143, 76, 95), colorkey=(255, 255, 255)))
                self.player_attack_sprite_southeast.append(
                    player_sprites.image_at((x + 20, 655, 76, 95), colorkey=(255, 255, 255)))
                self.player_attack_sprite_southwest.append(
                    player_sprites.image_at((x + 20, 911, 76, 95), colorkey=(255, 255, 255)))
            self.player_attack.append(self.player_attack_sprite_south)
            self.player_attack.append(self.player_attack_sprite_southwest)
            self.player_attack.append(self.player_attack_sprite_west)
            self.player_attack.append(self.player_attack_sprite_northwest)
            self.player_attack.append(self.player_attack_sprite_north)
            self.player_attack.append(self.player_attack_sprite_northeast)
            self.player_attack.append(self.player_attack_sprite_east)
            self.player_attack.append(self.player_attack_sprite_southeast)
        if not self.level10 and self.xp >= 81:
            self.level10 = True
            self.hp += 25
            player_sprites = spriteloader.spritesheet(os.path.join('images', 'lvl5player.png'))
            self.player_movement = []
            self.player_move_sprite_north = []
            self.player_move_sprite_south = []
            self.player_move_sprite_west = []
            self.player_move_sprite_east = []
            self.player_move_sprite_northwest = []
            self.player_move_sprite_northeast = []
            self.player_move_sprite_southeast = []
            self.player_move_sprite_southwest = []
            self.player_attack = []
            self.player_attack_sprite_north = []
            self.player_attack_sprite_south = []
            self.player_attack_sprite_west = []
            self.player_attack_sprite_east = []
            self.player_attack_sprite_northwest = []
            self.player_attack_sprite_northeast = []
            self.player_attack_sprite_southeast = []
            self.player_attack_sprite_southwest = []
            self.player_idle = []
            self.player_idle.append(player_sprites.image_at((20, 783, 76, 95), colorkey=(255, 255, 255)))
            self.player_idle.append(player_sprites.image_at((20, 911, 76, 95), colorkey=(255, 255, 255)))
            self.player_idle.append(player_sprites.image_at((20, 15, 76, 95), colorkey=(255, 255, 255)))
            self.player_idle.append(player_sprites.image_at((20, 143, 76, 95), colorkey=(255, 255, 255)))
            self.player_idle.append(player_sprites.image_at((20, 271, 76, 95), colorkey=(255, 255, 255)))
            self.player_idle.append(player_sprites.image_at((20, 399, 76, 95), colorkey=(255, 255, 255)))
            self.player_idle.append(player_sprites.image_at((20, 527, 76, 95), colorkey=(255, 255, 255)))
            self.player_idle.append(player_sprites.image_at((20, 655, 76, 95), colorkey=(255, 255, 255)))
            for x in range(512, 1536, 128):
                self.player_move_sprite_west.append(
                    player_sprites.image_at((x + 20, 15, 76, 95), colorkey=(255, 255, 255)))
                self.player_move_sprite_east.append(
                    player_sprites.image_at((x + 20, 527, 76, 95), colorkey=(255, 255, 255)))
                self.player_move_sprite_south.append(
                    player_sprites.image_at((x + 20, 783, 76, 95), colorkey=(255, 255, 255)))
                self.player_move_sprite_north.append(
                    player_sprites.image_at((x + 20, 271, 76, 95), colorkey=(255, 255, 255)))
                self.player_move_sprite_northeast.append(
                    player_sprites.image_at((x + 20, 399, 76, 95), colorkey=(255, 255, 255)))
                self.player_move_sprite_northwest.append(
                    player_sprites.image_at((x + 20, 143, 76, 95), colorkey=(255, 255, 255)))
                self.player_move_sprite_southeast.append(
                    player_sprites.image_at((x + 20, 655, 76, 95), colorkey=(255, 255, 255)))
                self.player_move_sprite_southwest.append(
                    player_sprites.image_at((x + 20, 911, 76, 95), colorkey=(255, 255, 255)))
            self.player_movement.append(self.player_move_sprite_south)
            self.player_movement.append(self.player_move_sprite_southwest)
            self.player_movement.append(self.player_move_sprite_west)
            self.player_movement.append(self.player_move_sprite_northwest)
            self.player_movement.append(self.player_move_sprite_north)
            self.player_movement.append(self.player_move_sprite_northeast)
            self.player_movement.append(self.player_move_sprite_east)
            self.player_movement.append(self.player_move_sprite_southeast)
            for x in range(1536, 2048, 128):
                self.player_attack_sprite_west.append(
                    player_sprites.image_at((x + 20, 15, 76, 95), colorkey=(255, 255, 255)))
                self.player_attack_sprite_east.append(
                    player_sprites.image_at((x + 20, 527, 76, 95), colorkey=(255, 255, 255)))
                self.player_attack_sprite_south.append(
                    player_sprites.image_at((x + 20, 783, 76, 95), colorkey=(255, 255, 255)))
                self.player_attack_sprite_north.append(
                    player_sprites.image_at((x + 20, 271, 76, 95), colorkey=(255, 255, 255)))
                self.player_attack_sprite_northeast.append(
                    player_sprites.image_at((x + 20, 399, 76, 95), colorkey=(255, 255, 255)))
                self.player_attack_sprite_northwest.append(
                    player_sprites.image_at((x + 20, 143, 76, 95), colorkey=(255, 255, 255)))
                self.player_attack_sprite_southeast.append(
                    player_sprites.image_at((x + 20, 655, 76, 95), colorkey=(255, 255, 255)))
                self.player_attack_sprite_southwest.append(
                    player_sprites.image_at((x + 20, 911, 76, 95), colorkey=(255, 255, 255)))
            self.player_attack.append(self.player_attack_sprite_south)
            self.player_attack.append(self.player_attack_sprite_southwest)
            self.player_attack.append(self.player_attack_sprite_west)
            self.player_attack.append(self.player_attack_sprite_northwest)
            self.player_attack.append(self.player_attack_sprite_north)
            self.player_attack.append(self.player_attack_sprite_northeast)
            self.player_attack.append(self.player_attack_sprite_east)
            self.player_attack.append(self.player_attack_sprite_southeast)

    def update(self, position, direction, action):
        if self.last_action != action:
            self.current_sprite = 0
            self.animation_timing = 0
        self.last_action = action
        if action == 0:
            self.current_sprite = 0
        if self.animation_timing < self.animation_speed:
            self.current_sprite += 1
            self.animation_timing += 1
        else:
            self.animation_timing = 0
        if action == 0:
            self.image = self.player_idle[direction]
        if action == 1:
            if self.current_sprite >= len(self.player_move_sprite_east):
                self.current_sprite = 0
        if action == 2:
            if self.current_sprite >= len(self.player_attack_sprite_north):
                self.current_sprite = 0
        if action == 1:
            self.image = self.player_movement[direction][self.current_sprite]
        elif action == 2:
            self.image = self.player_attack[direction][self.current_sprite]
        self.rect = self.image.get_rect(center=position)
        self.hitbox = self.rect.inflate(-13, -23)
        if direction == 0:
            x = 0
            y = 20
        elif direction == 1:
            x = -14
            y = 14
        elif direction == 2:
            x = -20
            y = 0
        elif direction == 3:
            x = -14
            y = -14
        elif direction == 4:
            x = -20
            y = 0
        elif direction == 5:
            x = 14
            y = -14
        elif direction == 6:
            x = 0
            y = 20
        else:
            x = 14
            y = 14
        self.damage_box = self.rect.inflate(20, 20).move(x, y)
