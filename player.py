import os

import pygame as pygame

import spriteloader


class Player(pygame.sprite.Sprite):
    hp = 100
    mana = 100
    damage = 4

    def __init__(self, position):
        super().__init__()
        movement = spriteloader.spritesheet(os.path.join('images', 'PlayerMovement.png'))
        attack = spriteloader.spritesheet(os.path.join('images', 'PlayerAttack.png'))
        self.last_action = 0
        self.player_movement = []
        self.player_move_sprite_up = []
        self.player_move_sprite_down = []
        self.player_move_sprite_left = []
        self.player_move_sprite_right = []
        self.player_attack = []
        self.player_attack_sprite_up = []
        self.player_attack_sprite_down = []
        self.player_attack_sprite_left = []
        self.player_attack_sprite_right = []
        for x in range(0, 768, 96):
            self.player_move_sprite_down.append(movement.image_at((x, 0, 62, 90), colorkey=(255, 255, 255)))
            self.player_move_sprite_left.append(movement.image_at((x, 194, 62, 90), colorkey=(255, 255, 255)))
            self.player_move_sprite_right.append(movement.image_at((x, 582, 62, 90), colorkey=(255, 255, 255)))
            self.player_move_sprite_up.append(movement.image_at((x, 388, 62, 90), colorkey=(255, 255, 255)))
        self.player_movement.append(self.player_move_sprite_down)
        self.player_movement.append(self.player_move_sprite_left)
        self.player_movement.append(self.player_move_sprite_up)
        self.player_movement.append(self.player_move_sprite_right)
        for x in range(0, 2048, 128):
            self.player_attack_sprite_down.append(attack.image_at((x, 943, 128, 95), colorkey=(255, 255, 255)))
            self.player_attack_sprite_left.append(attack.image_at((x, 169, 128, 95), colorkey=(255, 255, 255)))
            self.player_attack_sprite_right.append(attack.image_at((x, 685, 128, 95), colorkey=(255, 255, 255)))
            self.player_attack_sprite_up.append(attack.image_at((x, 427, 128, 95), colorkey=(255, 255, 255)))
        self.player_attack.append(self.player_attack_sprite_down)
        self.player_attack.append(self.player_attack_sprite_left)
        self.player_attack.append(self.player_attack_sprite_up)
        self.player_attack.append(self.player_attack_sprite_right)
        self.current_sprite = 0
        self.image = self.player_move_sprite_down[self.current_sprite]
        self.rect = self.image.get_rect(center=position)

    def lose_hp(self, damage):
        self.hp = self.hp - damage

    def update(self, position, direction, action):
        if self.last_action != action:
            self.current_sprite = 0
        self.last_action = action
        if action == 0:
            self.current_sprite = 0
        self.current_sprite += 1
        if action == 1:
            if self.current_sprite >= len(self.player_move_sprite_right):
                self.current_sprite = 0
        if action == 2:
            if self.current_sprite >= len(self.player_attack_sprite_up):
                self.current_sprite = 0
        if action == 1:
            self.image = self.player_movement[direction][self.current_sprite]
        elif action == 2:
            self.image = self.player_attack[direction][self.current_sprite]
        self.rect = self.image.get_rect(center=position)
