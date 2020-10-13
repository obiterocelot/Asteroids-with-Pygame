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
import math
import copy
from pygame.math import Vector2
from pygame.locals import (K_UP, K_LEFT, K_RIGHT)

import Bullet

screen_width = 800
screen_height = 600 #placeholder screensize
max_speed = 10 #this is the max speed for all sprites - including bullets
pygame.mixer.init()
thruster_sound = pygame.mixer.Sound("thrust.wav")
bullet_sound = pygame.mixer.Sound("fire.wav")

ADDINGEVENT = pygame.USEREVENT +2

class Player(pygame.sprite.Sprite):
    """this class defines the attributes of your controlable sprite"""
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((20, 25))
        pygame.draw.polygon(self.surf, (50, 120, 180), ((10, 0), (0, 25), (20, 25)))
        self.surf_copy = self.surf
        self.rect = self.surf.get_rect()
        self.accel = Vector2(0, -0.05)  # The acceleration Vector points upwards.
        self.pos = Vector2(screen_width / 2, screen_height / 2) #starting in the middle of the screen
        self.angle = 0
        self.turn_speed = 0
        self.speed = Vector2(0, 0)
        self.gun_accel = Vector2(0, -10)    #creation of the ship's gun
        self.immunity = True

    def immune(self, list1):
        """grants immunity for first two seconds on spawn"""
        if self.immunity == True: #checks if there is a player in the player_list
            pygame.time.set_timer(ADDINGEVENT, 2000)    #if not, it waits 2000 ms before it adds one to the list
        if self.immunity == False:
            pygame.time.set_timer(ADDINGEVENT, 0) #when one is added, it resets the counter to 0 so it doesn't keep making new players

    def update(self, pressed_keys):
        """updates the location of the sprite every frame if moved by keypress"""
        #pressing LEFT or RIGHT will start the player turning in the given direction
        if pressed_keys[K_LEFT]:
            self.turn_speed = -3 #can continue to change these ints to increase/decrease turn speed
            self.rotate()
        if pressed_keys[K_RIGHT]:
            self.turn_speed = 3
            self.rotate()
        #pressing up or down will increase or decrease the player speed by a factor of the acceleration
        if pressed_keys[K_UP]:
            thruster_sound.set_volume(0.05)
            thruster_sound.play()
            self.speed += self.accel

        #setting a max speed and adjusting the Vector to that max speed
        if self.speed.length() > max_speed:
            self.speed.scale_to_length(max_speed) #scales the direction down to the speed so it's not expontentially if you're going at an angle

        self.pos += self.speed  #updates the new player position to a factor of the given speed
        self.rect.center = self.pos     #updates the surface drawing to the new player position

    def rotate(self):
        """providing the rotation of the acceleration Vector"""
        self.accel.rotate_ip(self.turn_speed) #acceleration Vector is the one moving (speed is just by what factor)
        self.gun_accel.rotate_ip(self.turn_speed)
        self.angle += self.turn_speed #turn to a new angle as key is held down
        #this bit allows you to just go round and round in circles
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
        #transforms the ship sprite
        self.surf = pygame.transform.rotate(self.surf_copy, -self.angle)
        self.rect = self.surf.get_rect(center=self.rect.center)

    def get_gun_vec(self):
        """pull a copy of the gun vector on command"""
        return copy.deepcopy(self.gun_accel)    #this way the bullets wont turn as the ship turns

    def shoot(self, accel, list1, list2):
        """spawning your bullets"""
        if self.immunity == False:
            bullet = Bullet.Bullet(self.pos.x, self.pos.y, accel)
            bullet_sound.set_volume(0.1)
            bullet_sound.play()
            list1.add(bullet) #and adding them to the list
            list2.add(bullet)

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

def main():
    pass

if __name__ == '__main__':
    main()
