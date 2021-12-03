import os

import pygame as pygame

import spriteloader


class Npc(pygame.sprite.Sprite):

    def __init__(self, position, enemy_name):
        super().__init__()
        enemy_damage = {
            "Wyvern": 15,
            "Knight": 8,
            "Zombie": 6,
            "Demon": 12,
            "EvilPlayer": 20,
            "Hobgoblin": 14
        }
        enemy_hp = {
            "Wyvern": 40,
            "Knight": 14,
            "Zombie": 10,
            "Demon": 15,
            "Hobgoblin": 22,
            "EvilPlayer": 100
        }
        self.name = enemy_name
        self.damage = enemy_damage[enemy_name]
        self.hp = enemy_hp[enemy_name]
        enemy_sprites = spriteloader.spritesheet(os.path.join('images', enemy_name + 'Sprites.png'))
        self.xy = 128
        min_move = 512
        max_move = 1536
        min_attack = 1536
        max_attack = 2048
        doubled = 1
        if enemy_name == "Wyvern" or enemy_name == "Demon":
            min_move = min_move * 2
            max_move = max_move * 2
            min_attack = min_attack * 2
            max_attack = max_attack * 2
            self.xy = self.xy * 2
            doubled = 2
        self.last_action = 0
        self.animation_speed = 2
        self.animation_timing = 0
        self.enemy_movement = []
        self.enemy_move_sprite_north = []
        self.enemy_move_sprite_south = []
        self.enemy_move_sprite_west = []
        self.enemy_move_sprite_east = []
        self.enemy_move_sprite_northwest = []
        self.enemy_move_sprite_northeast = []
        self.enemy_move_sprite_southeast = []
        self.enemy_move_sprite_southwest = []
        self.enemy_attack = []
        self.enemy_attack_sprite_north = []
        self.enemy_attack_sprite_south = []
        self.enemy_attack_sprite_west = []
        self.enemy_attack_sprite_east = []
        self.enemy_attack_sprite_northwest = []
        self.enemy_attack_sprite_northeast = []
        self.enemy_attack_sprite_southeast = []
        self.enemy_attack_sprite_southwest = []
        self.enemy_idle = []
        self.enemy_idle.append(enemy_sprites.image_at((0, 768, self.xy, self.xy), colorkey=(255, 255, 255)))
        self.enemy_idle.append(enemy_sprites.image_at((0, 896, self.xy, self.xy), colorkey=(255, 255, 255)))
        self.enemy_idle.append(enemy_sprites.image_at((0, 0, self.xy, self.xy), colorkey=(255, 255, 255)))
        self.enemy_idle.append(enemy_sprites.image_at((0, 128, self.xy, self.xy), colorkey=(255, 255, 255)))
        self.enemy_idle.append(enemy_sprites.image_at((0, 256, self.xy, self.xy), colorkey=(255, 255, 255)))
        self.enemy_idle.append(enemy_sprites.image_at((0, 384, self.xy, self.xy), colorkey=(255, 255, 255)))
        self.enemy_idle.append(enemy_sprites.image_at((0, 512, self.xy, self.xy), colorkey=(255, 255, 255)))
        self.enemy_idle.append(enemy_sprites.image_at((0, 640, self.xy, self.xy), colorkey=(255, 255, 255)))
        for x in range(min_move, max_move, self.xy):
            self.enemy_move_sprite_west.append(enemy_sprites.image_at((x, 0, self.xy, self.xy), colorkey=(255, 255, 255)))
            self.enemy_move_sprite_east.append(
                enemy_sprites.image_at((x, 512 * doubled, self.xy, self.xy), colorkey=(255, 255, 255)))
            self.enemy_move_sprite_south.append(
                enemy_sprites.image_at((x, 768 * doubled, self.xy, self.xy), colorkey=(255, 255, 255)))
            self.enemy_move_sprite_north.append(
                enemy_sprites.image_at((x, 256 * doubled, self.xy, self.xy), colorkey=(255, 255, 255)))
            self.enemy_move_sprite_northeast.append(
                enemy_sprites.image_at((x, 384 * doubled, self.xy, self.xy), colorkey=(255, 255, 255)))
            self.enemy_move_sprite_northwest.append(
                enemy_sprites.image_at((x, 128 * doubled, self.xy, self.xy), colorkey=(255, 255, 255)))
            self.enemy_move_sprite_southeast.append(
                enemy_sprites.image_at((x, 640 * doubled, self.xy, self.xy), colorkey=(255, 255, 255)))
            self.enemy_move_sprite_southwest.append(
                enemy_sprites.image_at((x, 896 * doubled, self.xy, self.xy), colorkey=(255, 255, 255)))
        self.enemy_movement.append(self.enemy_move_sprite_south)
        self.enemy_movement.append(self.enemy_move_sprite_southwest)
        self.enemy_movement.append(self.enemy_move_sprite_west)
        self.enemy_movement.append(self.enemy_move_sprite_northwest)
        self.enemy_movement.append(self.enemy_move_sprite_north)
        self.enemy_movement.append(self.enemy_move_sprite_northeast)
        self.enemy_movement.append(self.enemy_move_sprite_east)
        self.enemy_movement.append(self.enemy_move_sprite_southeast)
        for x in range(min_attack, max_attack, self.xy):
            self.enemy_attack_sprite_west.append(
                enemy_sprites.image_at((x, 0, self.xy, self.xy), colorkey=(255, 255, 255)))
            self.enemy_attack_sprite_east.append(
                enemy_sprites.image_at((x, 512 * doubled, self.xy, self.xy), colorkey=(255, 255, 255)))
            self.enemy_attack_sprite_south.append(
                enemy_sprites.image_at((x, 768 * doubled, self.xy, self.xy), colorkey=(255, 255, 255)))
            self.enemy_attack_sprite_north.append(
                enemy_sprites.image_at((x, 256 * doubled, self.xy, self.xy), colorkey=(255, 255, 255)))
            self.enemy_attack_sprite_northeast.append(
                enemy_sprites.image_at((x, 384 * doubled, self.xy, self.xy), colorkey=(255, 255, 255)))
            self.enemy_attack_sprite_northwest.append(
                enemy_sprites.image_at((x, 128 * doubled, self.xy, self.xy), colorkey=(255, 255, 255)))
            self.enemy_attack_sprite_southeast.append(
                enemy_sprites.image_at((x, 640 * doubled, self.xy, self.xy), colorkey=(255, 255, 255)))
            self.enemy_attack_sprite_southwest.append(
                enemy_sprites.image_at((x, 896 * doubled, self.xy, self.xy), colorkey=(255, 255, 255)))
        self.enemy_attack.append(self.enemy_attack_sprite_south)
        self.enemy_attack.append(self.enemy_attack_sprite_southwest)
        self.enemy_attack.append(self.enemy_attack_sprite_west)
        self.enemy_attack.append(self.enemy_attack_sprite_northwest)
        self.enemy_attack.append(self.enemy_attack_sprite_north)
        self.enemy_attack.append(self.enemy_attack_sprite_northeast)
        self.enemy_attack.append(self.enemy_attack_sprite_east)
        self.enemy_attack.append(self.enemy_attack_sprite_southeast)
        self.current_sprite = 0
        self.image = self.enemy_move_sprite_south[self.current_sprite]
        self.rect = self.image.get_rect(center=position)
        self.hitbox = self.rect.inflate(-2 * self.xy/3, -2 * self.xy/3)

    def update(self, position, direction, action=1):
        self.last_action = action
        if action == 0:
            self.current_sprite = 0
            self.animation_timing = 0
        if self.animation_timing < self.animation_speed:
            self.animation_timing += 1
        else:
            self.current_sprite += 1
            self.animation_timing = 0
        if action == 0:
            self.image = self.enemy_idle[direction]
        if action == 1:
            if self.current_sprite >= len(self.enemy_move_sprite_south):
                self.current_sprite = 0
        if action == 2:
            if self.current_sprite >= len(self.enemy_attack_sprite_south):
                self.current_sprite = 0
        if action == 1:
            self.image = self.enemy_movement[direction][self.current_sprite]
        elif action == 2:
            self.image = self.enemy_attack[direction][self.current_sprite]
        self.rect = self.image.get_rect(center=position)
        self.hitbox = self.rect.inflate(-2 * self.xy/3, -2 * self.xy/3)

    def take_damage(self, damage):
        self.hp -= damage
