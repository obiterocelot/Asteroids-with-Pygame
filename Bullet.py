#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sarah
#
# Created:     13/10/2020
# Copyright:   (c) sarah 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame
from pygame.math import Vector2

screen_width = 800
screen_height = 600 #placeholder screensize
max_speed = 10 #this is the max speed for all sprites - including bullets

class Bullet(pygame.sprite.Sprite):
    """this class defines the bullets that your controlable sprite fires"""
    def __init__(self, x, y, accel):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((5, 5))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(100, 100))
        self.pos = Vector2(x, y) #let's start in the middle of the screen
        self.accel = accel #this is the pulled number from the ship's gun vector. Find this pull on the space key command

    def update(self):
        """updates the location of the sprite every frame. Incl kill command"""
        self.pos += self.accel
        self.rect.center = self.pos
        #kill the bullet once off screen to keep game slick
        if self.pos.x > screen_width or self.pos.x < 0:
            self.kill()
        if self.pos.y > screen_height or self.pos.y <= 0:
            self.kill()
        if self.accel.length() > max_speed -1: #scale to keep a consistent speed. 1 less lower than max speed of ship is a figure found from studies of original asteroids(link above)
            self.accel.scale_to_length(max_speed -1)

def main():
    pass

if __name__ == '__main__':
    main()
