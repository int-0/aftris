#!/usr/bin/env python

import pygame

class Keyboard(object):
    def __init__(self, game):
        self.__game = game

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.__game.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.__game.move_right()
                elif event.key == pygame.K_DOWN:
                    self.__game.move_down()
                elif event.key == pygame.K_UP:
                    self.__game.rotate_CW()
                elif event.key == pygame.K_SPACE:
                    self.__game.drop_piece()
                elif event.key == pygame.K_ESCAPE:
                    self.__game.quit()
