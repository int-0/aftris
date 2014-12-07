#!/usr/bin/env python

import pygame

class EventDispatcher(object):
    def __init__(self):
        self.__key_down_listeners = []
        self.__key_up_listeners = []

    def add_key_down_listener(self, listener):
        self.__key_down_listeners.append(listener)

    def add_key_up_listener(self, listener):
        self.__key_up_listeners.append(listener)

    def update(self):
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                for listener in self.__key_down_listeners:
                    listener.refresh(event.key)
            if (event.type == pygame.KEYUP):
                for listener in self.__key_up_listeners:
                    listener.refresh(event.key)
                    

class Listener(object):
    def __init__(self):
        self.__last_data = None

    @property
    def last(self):
        return self.__last_data
    
    def refresh(self, event_data):
        self.__last_data = event_data


class Controller(Listener):
    def __init__(self, game=None):
        Listener.__init__(self)
        self.__game = game

    def control(self, game):
        self.__game = game
        
    @property
    def controlled_game(self):
        return self.__game


class Player1(Controller):
    def __init__(self, game=None):
        Controller.__init__(self, game)

    def refresh(self, key):
        if self.controlled_game is None:
            return
        if key == pygame.K_LEFT:
            self.controlled_game.move_left()
        elif key == pygame.K_RIGHT:
            self.controlled_game.move_right()
        elif key == pygame.K_DOWN:
            self.controlled_game.move_down()
        elif key == pygame.K_UP:
            self.controlled_game.rotate_CW()
        elif key == pygame.K_SPACE:
            self.controlled_game.drop_piece()
        elif key == pygame.K_ESCAPE:
            self.controlled_game.quit()
