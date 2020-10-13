#-------------------------------------------------------------------------------
# Name:        AsteroidsPyGame.py
# Purpose:     education
# Author:      sarah
# Created:     15/09/2020
# Copyright:   (c) sarah 2020
# Licence:     coding help on Vectors: https://stackoverflow.com/questions/48856922/pygame-how-to-make-sprite-move-in-the-direction-its-facing-with-vectors
#              help with structure of game loop: https://pythonprogramming.net/pygame-start-menu-tutorial/
#              Figures on appropriate sizes of sprites etc: http://www.retrogamedeconstructionzone.com/2019/10/asteroids-by-numbers.html
#-------------------------------------------------------------------------------

import pygame
import math
import copy

from Asteroid import (Asteroid_BIG, Asteroid_MED, Asteroid_SML)
import Bullet
from Player import Player

from pygame.locals import (RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_SPACE, KEYDOWN, KEYUP, QUIT, MOUSEBUTTONDOWN)
from pygame.math import Vector2

screen_width = 800
screen_height = 600 #placeholder screensize
max_speed = 10 #this is the max speed for all sprites - including bullets
ADDINGEVENT = pygame.USEREVENT +2
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.mixer.init()
asteroid_sound = pygame.mixer.Sound("bangLarge.wav")
ship_sound = pygame.mixer.Sound("bangSmall.wav")

def setup():
    pygame.init()
    pygame.mixer.init()

    start = True
    while start:

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    start = False
            elif event.type == QUIT:
                pygame.quit()
                start = False
            if event.type == MOUSEBUTTONDOWN:
                start = False

        if start:
            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 100)
            text = font.render("ASTEROIDS", 1, (255, 255, 255))
            screen.blit(text, (50, 100))
            pygame.display.update()
            clock.tick(15)

def main():

    score = 0 #the first set up of the score
    lives = 3 #first step of setting up a life counter

    addasteroid = pygame.USEREVENT +1
    pygame.time.set_timer(addasteroid, 2000) #creation of the event to add a Big Asteroid
    maximum_enemies = 5 #fill in figure. TO ADJUST LATER

    #group lists
    player = Player() #creates a character at the first instance
    bullets_list = pygame.sprite.Group()
    asteroids_big = pygame.sprite.Group()
    asteroids_med = pygame.sprite.Group()
    asteroids_sml = pygame.sprite.Group()
    all_asteroids = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    player_list = pygame.sprite.Group()
    all_sprites.add(player) #add the player to the all_sprites list so its blitted onto the screen
    player.immune(player_list)  #grants the character immunity

    running = True
    while running:

    #quit protocols
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    running = False
            elif event.type == QUIT:
                pygame.quit()
                running = False

            if event.type == KEYDOWN and event.key == K_SPACE:
                """shooting the gun"""
                gun = player.get_gun_vec()
                player.shoot(gun, all_sprites, bullets_list)

            if event.type == addasteroid:
                """spawning new asteroids"""
                if len(asteroids_big) < maximum_enemies and len(all_asteroids) < 7:
                    new_asteroid = Asteroid_BIG()
                    asteroids_big.add(new_asteroid)
                    all_asteroids.add(new_asteroid)
                    all_sprites.add(new_asteroid)

            if event.type == ADDINGEVENT:
                player_list.add(player) #adding the player to the player_list where it will recognise a collision with an asteroid
                player.immunity = False

        def asteroid_hit(death, accel, new_astsize, new_list, counter=0):
            """definition of what happens at an asteroid death and split. Small Asteroid is different"""
            if counter < 2:
                new_asteroid = new_astsize(accel, Vector2(death))   #essentially, creates a new list from the death accel pulled before def is called
                asteroid_sound.set_volume(0.1)
                asteroid_sound.play()
                all_asteroids.add(new_asteroid) #... and adds it to the necessary lists
                new_list.add(new_asteroid)
                all_sprites.add(new_asteroid)
                accel2 = copy.deepcopy(accel)   #makes a copy of the accel (else both asteroids would use the same Vector)
                counter += 1    #only needs to happen twice
                asteroid_hit(death, accel2, new_astsize, new_list, counter) #and does it again

    #definiting hits of asteroids by bullets
        """BIG"""
        asteroid_big_hit = pygame.sprite.groupcollide(asteroids_big, bullets_list, True, pygame.sprite.collide_circle)
        for hit in asteroid_big_hit:
            death = hit.death_pos() #had to pull death and accel before def. Pulling hit would turn it into a list instead of a class
            accel = copy.deepcopy(hit.death_accel())
            asteroid_hit(death, accel, Asteroid_MED, asteroids_med)
            score += 20 #score values taken from original asteroid game

        """MED"""
        asteroid_med_hit = pygame.sprite.groupcollide(asteroids_med, bullets_list, True, pygame.sprite.collide_circle)
        for hit in asteroid_med_hit:
            death = hit.death_pos()
            accel = copy.deepcopy(hit.death_accel())
            asteroid_hit(death, accel, Asteroid_SML, asteroids_sml)
            score += 50

        """SML"""
        asteroid_sml_hit = pygame.sprite.groupcollide(asteroids_sml, bullets_list, True, pygame.sprite.collide_circle)
        for hit in asteroid_sml_hit:
            score += 100

        player_hit = pygame.sprite.groupcollide(player_list, all_asteroids, True, pygame.sprite.collide_circle)
        for hit in player_hit:
            lives -= 1  #takes a life (currently only a counter)
            ship_sound.set_volume(0.1)
            ship_sound.play()
            player = player.kill()
            player = Player()
            all_sprites.add(player)
            player.immune(player_list)

        if lives == 0:
            running = False

        if running:
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

    #placeholder for lives
            font = pygame.font.Font(None, 20)
            text = font.render(str(lives), 1, (255, 255, 255))
            screen.blit(text, (40, 10))

            pygame.display.flip()

            clock.tick(60)

def game_over():
    end = True
    while end:

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    end = False
            elif event.type == QUIT:
                pygame.quit()
                end = False
            if event.type == MOUSEBUTTONDOWN:
                main()

        if end:
            screen.fill((0, 0, 0))
            font1 = pygame.font.Font(None, 100)
            font2 = pygame.font.Font(None, 50)
            text1 = font1.render("GAME OVER.", 1, (255, 255, 255))
            text2 = font2.render("click to play again", 1, (255, 255, 255))
            screen.blit(text1, (50, 100))
            screen.blit(text2, (50, 250))
            pygame.display.update()
            clock.tick(15)

setup()
main()
game_over()
pygame.quit()