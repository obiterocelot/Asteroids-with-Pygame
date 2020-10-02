#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sarah
#
# Created:     15/09/2020
# Copyright:   (c) sarah 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame
import math

from pygame.locals import (RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, KEYUP, QUIT)
from pygame.math import Vector2

screen_width = 800
screen_height = 600 #placeholder screensize

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
        if self.speed.length() > 10:
            self.speed.scale_to_length(10) #scales the direction down to the speed so it's not expontentially if you're going at an angle

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

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height))

player = Player()

running = True
while running:
    #quit protocols
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    #player movement
    pressed_keys = pygame.key.get_pressed()
    player.screen_wrap()
    player.update(pressed_keys)

    screen.fill((0, 0, 0)) #black

    screen.blit(player.surf, player.rect)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()