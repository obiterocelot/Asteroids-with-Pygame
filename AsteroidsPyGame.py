#-------------------------------------------------------------------------------
# Name:        AsteroidsPyGame.py
# Purpose:     education
# Author:      sarah
# Created:     15/09/2020
# Copyright:   (c) sarah 2020
# Licence:     coding help on Vectors: https://stackoverflow.com/questions/48856922/pygame-how-to-make-sprite-move-in-the-direction-its-facing-with-vectors
#-------------------------------------------------------------------------------

import pygame
import math

from pygame.locals import (RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_SPACE, KEYDOWN, KEYUP, QUIT)
from pygame.math import Vector2

screen_width = 800
screen_height = 600 #placeholder screensize

max_speed = 10 #this is the max speed for all sprites - including bullets

class Player(pygame.sprite.Sprite):
    """this class defines the attributes of your controlable sprite"""
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((70, 50))
        pygame.draw.polygon(self.surf, (50, 120, 180), ((35, 0), (0, 35), (70, 35)))
        self.surf_copy = self.surf
        self.rect = self.surf.get_rect()
        self.pos = Vector2(screen_width / 2, screen_height / 2) #let's start in the middle of the screen
        self.accel = Vector2(0, -0.05)  # The acceleration Vector points upwards.
        self.angle = 0
        self.turn_speed = 0
        self.speed = Vector2(0, 0)

    def update(self, pressed_keys):
        """updates the location of the sprite every frame if moved by keypress"""
        #pressing LEFT or RIGHT will start the player turning in the given direction
        if pressed_keys[K_LEFT]:
            self.turn_speed = -3 #can continue to change these ints to increase/decrease turn speed
            player.rotate()
        if pressed_keys[K_RIGHT]:
            self.turn_speed = 3
            player.rotate()
        #pressing up or down will increase or decrease the player speed by a factor of the acceleration
        if pressed_keys[K_UP]:
            self.speed += self.accel

        #setting a max speed and adjusting the Vector to that max speed
        if self.speed.length() > max_speed:
            self.speed.scale_to_length(max_speed) #scales the direction down to the speed so it's not expontentially if you're going at an angle

        self.pos += self.speed  #updates the new player position to a factor of the given speed
        self.rect.center = self.pos     #updates the surface drawing to the new player position


    def rotate(self):
        """providing the rotation of the acceleration Vector"""
        self.accel.rotate_ip(self.turn_speed) #acceleration Vector is the one moving (speed is just by what factor)
        self.angle += self.turn_speed #turn to a new angle as key is held down
        #this bit allows you to just go round and round in circles
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
        self.surf = pygame.transform.rotate(self.surf_copy, -self.angle)
        self.rect = self.surf.get_rect(center=self.rect.center)

    def shoot(self):
        bullet = Bullet(self.pos.x, self.pos.y)
        all_sprites.add(bullet)
        bullets_list.add(bullet)

    def screen_wrap(self):
        """rules for player wrapping around screen (each sprite is a little different)"""
        if self.pos.x > screen_width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = screen_width
        if self.pos.y <= 0:
            self.pos.y = screen_height
        if self.pos.y > screen_height:
            self.pos.y = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((5, 5))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.speed = Vector2(0, -max_speed)
        self.pos = Vector2(x, y)

    def update(self):
        self.pos += self.speed
        self.rect.center = self.pos
        if self.pos.x > screen_width or self.pos.x < 0:
            self.kill()
        if self.pos.y > screen_height or self.pos.y <= 0:
            self.kill()

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height))

player = Player()
bullets_list = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
while running:
    #quit protocols
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        if event.type == KEYDOWN and event.key == K_SPACE:
            player.shoot()

    #player movement
    pressed_keys = pygame.key.get_pressed()
    player.screen_wrap()
    player.update(pressed_keys)
    bullets_list.update()

    screen.fill((0, 0, 0)) #black

    for each in all_sprites:
        screen.blit(each.surf, each.rect)

    for each in bullets_list:
        screen.blit(each.surf, each.rect)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()