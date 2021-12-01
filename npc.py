import os

import pygame as pygame

import spriteloader


class Npc(pygame.sprite.Sprite):

    def __init__(self, position, enemy_name):
        super().__init__()
        self.damage = 1
        self.hp = 10
        movement = spriteloader.spritesheet(os.path.join('images', enemy_name + 'Movement.png'))
        self.last_action = 0
        self.enemy_movement = []
        self.enemy_move_sprite_up = []
        self.enemy_move_sprite_down = []
        self.enemy_move_sprite_left = []
        self.enemy_move_sprite_right = []
        for x in range(0, 3072, 128):
            self.enemy_move_sprite_down.append(movement.image_at((x + 34, 22, 48, 74), colorkey=(255, 255, 255)))
            self.enemy_move_sprite_left.append(movement.image_at((x + 34, 216, 48, 74), colorkey=(255, 255, 255)))
            self.enemy_move_sprite_right.append(movement.image_at((x + 34, 604, 48, 74), colorkey=(255, 255, 255)))
            self.enemy_move_sprite_up.append(movement.image_at((x + 34, 410, 48, 74), colorkey=(255, 255, 255)))
        self.enemy_movement.append(self.enemy_move_sprite_down)
        self.enemy_movement.append(self.enemy_move_sprite_left)
        self.enemy_movement.append(self.enemy_move_sprite_up)
        self.enemy_movement.append(self.enemy_move_sprite_right)
        self.current_sprite = 0
        self.image = self.enemy_move_sprite_down[self.current_sprite]
        self.rect = self.image.get_rect(center=position)
        self.hitbox = self.rect.inflate(-50, -50)

    def update(self, position, direction, action=1):
        self.last_action = action
        if action == 0:
            self.current_sprite = 0
        self.current_sprite += 1
        if action == 1:
            if self.current_sprite >= len(self.enemy_move_sprite_left):
                self.current_sprite = 0
        if action == 2:
            if self.current_sprite >= len(self.enemy_move_sprite_up):
                self.current_sprite = 0
        if action == 1:
            self.image = self.enemy_movement[direction][self.current_sprite]
        elif action == 2:
            self.image = self.enemy_movement[direction][self.current_sprite]
        self.rect = self.image.get_rect(center=position)
        self.hitbox = self.rect.inflate(-10, -10)

    def take_damage(self, damage):
        self.hp -= damage
