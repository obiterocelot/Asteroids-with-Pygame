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
import random
from pygame.math import Vector2
from pygame.locals import RLEACCEL
import copy

screen_width = 800
screen_height = 600 #placeholder screensize

class Asteroid(pygame.sprite.Sprite):
    """Asteroid parent class"""
    def __init__(self, image, position, acceleration, speed):
        #all asteroids have the same features, but different sizes of those features. The children classes define those sizes and any extra features
        super(Asteroid, self).__init__()
        self.surf = pygame.image.load(image).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.pos = position
        self.accel = acceleration
        self.speed = Vector2(0, -1) #speed is an increasing upwards momentum. When scaled down by the max_speed, it allows you to set different speeds for the asteroids
        self.max_speed = speed

    def death_pos(self):    #The asteroid.death_pos and death_accel are necessary figures to spawn the new kinds of asteroids on death
        """position at moment of collision with Bullet class"""
        return copy.deepcopy(self.pos)

    def death_accel(self):
        """acceleration/direction at moment of collision with Bullet class"""
        return copy.deepcopy(self.accel)

    def update(self):
        self.speed += self.accel #continue to update accel to a factor of the speed...

        if self.speed.length() > self.max_speed: #then scale it to the max_speed.
            self.speed.scale_to_length(self.max_speed)

        self.pos += self.speed
        self.rect.center = self.pos

        #screen wrap rules below allow. +/- 40 allow for smoother transition
        if self.pos.x > screen_width + 40:
            self.pos.x = -40
        if self.pos.x < -40:
            self.pos.x = screen_width + 40
        if self.pos.y <= -40:
            self.pos.y = screen_height + 40
        if self.pos.y > screen_height + 40:
            self.pos.y = -40

class Asteroid_BIG(Asteroid):
    """Big Asteroid subclass of Asteroid"""
    def __init__(self):
        image = "asteroid1_L.png"
        position = self.starting_pos() #randomly generated off screen starter.
        acceleration = Vector2(0, -1) #needs a starting accel to turn
        speed = 1
        super(Asteroid_BIG, self).__init__(image, position, acceleration, speed) #individually broken down so I can more easily adjust at a later date if need be.
        self.accel.rotate_ip(random.randint(0, 360)) #random turn is in children classes so as to give some illusion of momentum.

    def starting_pos(self):
        """provides a random off-screen starting position"""
        #starting positions are split into quadrants. starting_pos randomly generates a point position from each quadrant, then one of the quadrants is randomly selected.
        left = (random.randint(-80, -40), random.randint(-80, (screen_height + 80))) #quadrants are all the same size off-screen
        right = (random.randint((screen_width + 40), (screen_width + 80)), random.randint(-80, (screen_height + 80)))
        top = (random.randint(-80, (screen_width + 80)), random.randint(-80, -40))
        bottom = (random.randint(-80, (screen_width +80)), random.randint(screen_height + 40, screen_height + 80))
        list = [left, right, top, bottom] #list of the four quadrants
        return random.choice(list) #random.choice picks one of the 4 options at random.

class Asteroid_MED(Asteroid):
    """Medium Asteroid subclass of Asteroid"""
    def __init__(self, accel, death):
        image = "asteroid1_M.png"
        position = death
        acceleration = accel
        speed = 2
        super(Asteroid_MED, self).__init__(image, position, acceleration, speed)
        self.accel.rotate_ip(random.randint(0, 90)) #can only turn a maximum of 90 degrees from the direction it was going.

class Asteroid_SML(Asteroid):
    """Small Asteroid subclass of Asteroid"""
    def __init__(self, accel, death):
        image = "asteroid1_S.png"
        position = death
        acceleration = accel
        speed = 2.5 #3 is a bit fast
        super(Asteroid_SML, self).__init__(image, position, acceleration, speed)
        self.accel.rotate_ip(random.randint(0, 90))

def main():
    pass

if __name__ == '__main__':
    main()
