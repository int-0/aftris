#!/usr/bin/env python

import game

LINES_TO_SPEED_UP = 10

class Forever(object):
    def __init__(self, size=game.DEFAULT_SIZE, initial_speed=game.DEFAULT_SPEED):
        self.__game = game.Tetris(size, initial_speed)

        self.__score = 0
        self.__lines = 0

        self.__lines_to_speed_up = LINES_TO_SPEED_UP

    @property
    def game(self):
        return self.__game

    @property
    def game_over(self):
        return self.__game.game_over

    @property
    def score(self):
        return self.__score

    @property
    def lines(self):
        return self.__lines

    def update(self):
        lines = self.game.update()

        self.__score += lines * lines * 10
        self.__lines += lines

        self.__lines_to_speed_up -= lines
        if self.__lines_to_speed_up < 0:
            self.__lines_to_speed_up = LINES_TO_SPEED_UP
            self.__game.increase_speed(10)
