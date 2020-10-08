#-------------------------------------------------------------------------------
# Name:        AsteroidsPyGame.py
# Purpose:     education
# Author:      sarah
# Created:     15/09/2020
# Copyright:   (c) sarah 2020
# Licence:     coding help on Vectors: https://stackoverflow.com/questions/48856922/pygame-how-to-make-sprite-move-in-the-direction-its-facing-with-vectors
#               Figures on appropriate sizes of sprites etc: http://www.retrogamedeconstructionzone.com/2019/10/asteroids-by-numbers.html
#-------------------------------------------------------------------------------

import pygame
import math
import copy
import random

from pygame.locals import (RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_SPACE, KEYDOWN, KEYUP, QUIT)
from pygame.math import Vector2

screen_width = 800
screen_height = 600 #placeholder screensize

max_speed = 10 #this is the max speed for all sprites - including bullets

class Player(pygame.sprite.Sprite):
    """this class defines the attributes of your controlable sprite"""
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((20, 25))
        pygame.draw.polygon(self.surf, (50, 120, 180), ((10, 0), (0, 25), (20, 25)))
        self.surf_copy = self.surf
        self.rect = self.surf.get_rect()
        self.pos = Vector2(screen_width / 2, screen_height / 2) #let's start in the middle of the screen
        self.accel = Vector2(0, -0.05)  # The acceleration Vector points upwards.
        self.angle = 0
        self.turn_speed = 0
        self.speed = Vector2(0, 0)
        self.gun_accel = Vector2(0, -10)    #creation of the ship's gun

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

    def shoot(self, accel):
        """spawning your bullets"""
        bullet = Bullet(self.pos.x, self.pos.y, accel)
        all_sprites.add(bullet) #and adding them to the list
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

class Asteroid(pygame.sprite.Sprite):
    """Asteroid parent class"""
    def __init__(self, surf_size, circle_size, color, position, acceleration, speed):
        #all asteroids have the same features, but different sizes of those features. The children classes define those sizes and any extra features
        super(Asteroid, self).__init__()
        self.surf = pygame.Surface(surf_size)
        pygame.draw.circle(self.surf, (color), (circle_size), circle_size[0], 2)
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
        surf_size = (80, 80)
        circle_size = (40, 40)
        color = (255, 192, 203)
        position = self.starting_pos() #randomly generated off screen starter.
        acceleration = Vector2(0, -1) #needs a starting accel to turn
        speed = 1
        super(Asteroid_BIG, self).__init__(surf_size, circle_size, color, position, acceleration, speed) #individually broken down so I can more easily adjust at a later date if need be.
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
        surf_size = (40, 40)
        circle_size = (20, 20)
        color = (0, 255, 0)
        position = death
        acceleration = accel
        speed = 2
        super(Asteroid_MED, self).__init__(surf_size, circle_size, color, position, acceleration, speed)
        self.accel.rotate_ip(random.randint(0, 90)) #can only turn a maximum of 90 degrees from the direction it was going.

class Asteroid_SML(Asteroid):
    """Small Asteroid subclass of Asteroid"""
    def __init__(self, accel, death):
        surf_size = (20, 20)
        circle_size = (10, 10)
        color = (255,255,153)
        position = death
        acceleration = accel
        speed = 2.5 #3 is a bit fast
        super(Asteroid_SML, self).__init__(surf_size, circle_size, color, position, acceleration, speed)
        self.accel.rotate_ip(random.randint(0, 90))

def asteroid_hit(death, accel, new_astsize, new_list, counter=0):
    """definition of what happens at an asteroid death and split. Small Asteroid is different"""
    if counter < 2:
        new_asteroid = new_astsize(accel, Vector2(death))   #essentially, creates a new list from the death accel pulled before def is called
        all_asteroids.add(new_asteroid) #... and adds it to the necessary lists
        new_list.add(new_asteroid)
        all_sprites.add(new_asteroid)
        accel2 = copy.deepcopy(accel)   #makes a copy of the accel (else both asteroids would use the same Vector)
        counter += 1    #only needs to happen twice
        asteroid_hit(death, accel2, new_astsize, new_list, counter) #and does it again
    else:
        return

pygame.init()

clock = pygame.time.Clock() #required for events that need a timer

score = 0 #the first set up of the score

screen = pygame.display.set_mode((screen_width, screen_height))

addasteroid = pygame.USEREVENT +1
pygame.time.set_timer(addasteroid, 2000) #creation of the event to add a Big Asteroid
maximum_enemies = 5 #fill in figure. TO ADJUST LATER

#group lists
player = Player()
bullets_list = pygame.sprite.Group()
asteroids_big = pygame.sprite.Group()
asteroids_med = pygame.sprite.Group()
asteroids_sml = pygame.sprite.Group()
all_asteroids = pygame.sprite.Group()
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
            """shooting the gun"""
            gun = player.get_gun_vec()
            player.shoot(gun)

        if event.type == addasteroid:
            """spawning new asteroids"""
            if len(asteroids_big) < maximum_enemies and len(all_asteroids) < 7:
                new_asteroid = Asteroid_BIG()
                asteroids_big.add(new_asteroid)
                all_asteroids.add(new_asteroid)
                all_sprites.add(new_asteroid)

    #definiting hits of asteroids by bullets
    """BIG"""
    asteroid_big_hit = pygame.sprite.groupcollide(asteroids_big, bullets_list, True, pygame.sprite.collide_circle)
    for hit in asteroid_big_hit:
        death = hit.death_pos() #had to pull death and accel before def. Pulling hit would turn it into a list instead of a class
        accel = copy.deepcopy(hit.death_accel())
        asteroid_hit(death, accel, Asteroid_MED, asteroids_med)

    """MED"""
    asteroid_med_hit = pygame.sprite.groupcollide(asteroids_med, bullets_list, True, pygame.sprite.collide_circle)
    for hit in asteroid_med_hit:
        death = hit.death_pos()
        accel = copy.deepcopy(hit.death_accel())
        asteroid_hit(death, accel, Asteroid_SML, asteroids_sml)

    """SML"""
    asteroid_sml_hit = pygame.sprite.groupcollide(asteroids_sml, bullets_list, True, pygame.sprite.collide_circle)
    for hit in asteroid_sml_hit:
        score += 1

    #player movement
    pressed_keys = pygame.key.get_pressed()
    player.screen_wrap()
    bullets_list.update()
    player.update(pressed_keys)
    all_asteroids.update()

    screen.fill((0, 0, 0)) #black

    for each in all_sprites: #drawing everything
        screen.blit(each.surf, each.rect)

    #below is a placeholder for the score
    font = pygame.font.Font(None, 20)
    text = font.render(str(score), 1, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()