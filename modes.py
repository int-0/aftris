#!/usr/bin/env python

import game
import pygame

LINES_TO_SPEED_UP = 10

BACKGROUNDS = [
    pygame.image.load('res/ingamegnd.png'),
    pygame.image.load('res/ingamegnd2.png')
]

LINES_TO_CYCLE = 19

class Forever(object):
    def __init__(self, size=game.DEFAULT_SIZE,
                 initial_speed=game.DEFAULT_SPEED,
                 change_bckgnd_callback=None):
        self.__game = game.Tetris(size, initial_speed)

        self.__score = 0
        self.__lines = 0

        self.__change_background = change_bckgnd_callback
        self.__lines_to_cycle = LINES_TO_CYCLE
        self.__current_background = 0
        
        self.__lines_to_speed_up = LINES_TO_SPEED_UP

    @property
    def show_next(self):
        return True

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

        self.__lines_to_cycle -= lines
        if self.__lines_to_cycle < 0:
            self.__lines_to_cycle = LINES_TO_CYCLE
            if self.__change_background is not None:
                self.__current_background += 1
                self.__current_background %= len(BACKGROUNDS)
                self.__change_background(BACKGROUNDS[self.__current_background])


class Stage(object):
    def __init__(self, definition={
            'speed_var': game.DEFAULT_SPEED,
            'extra_blocks': [],
            'lines_to_go': 10,
            'show_next': True,
            'background': None}):
        self.speed = definition['speed_var']
        self.extra_blocks = definition['extra_blocks']
        self.lines_to_go = definition['lines_to_go']
        self.show_next = definition['show_next']
        self.background = definition['background']

    def add_block(self, position, color):
        self.extra_blocks.append((position, color))

    @property
    def as_dict(self):
        return {
            'speed_var': self.speed,
            'extra_blocks': self.extra_blocks,
            'lines_to_go': self.lines_to_go,
            'show_next': self.show_next,
            'background': self.background
        }


class Levels(object):
    def __init__(self, size=game.DEFAULT_SIZE,
                 initial_speed=game.DEFAULT_SPEED,
                 stages=[Stage()],
                 start_level_callback=None,
                 end_level_callback=None,
                 change_bckgnd_callback=None):
        self.__game = game.Tetris(size, initial_speed)

        self.__score = 0
        self.__lines = 0

        self.__lines_to_go = 0
        self.__current_stage = 0
        self.__show_next = True
        self.__stages = stages
        self.__game_completed = False

        self.__start_level = start_level_callback
        self.__end_level = end_level_callback
        self.__change_background = change_bckgnd_callback
        self.load_level(self.__current_stage)


    @property
    def show_next(self):
        return self.__show_next

    @property
    def game(self):
        return self.__game

    @property
    def game_over(self):
        return self.__game.game_over

    @property
    def completed(self):
        return self.__game_completed

    @property
    def score(self):
        return self.__score

    def load_level(self, level_no):
        # Avoid invalid levels
        if level_no not in range(len(self.__stages)):
            return False
        self.__current_stage = level_no
        level = self.__stages[self.__current_stage]
        new_speed = self.game.speed + level.speed
        self.__game = game.Tetris(self.__game.size, new_speed)
        for position, block in level.extra_blocks:
            self.__game.board[position[1]][position[0]] = block
        self.__show_next = level.show_next
        self.__lines_to_go = level.lines_to_go
        if level.background:
            self.__change_background(level.background)
        if self.__start_level:
            self.__start_level(level_no)
        return True

    @property
    def lines(self):
        return self.__lines

    def update(self):
        if self.completed:
            return
        lines = self.game.update()
        self.__score += lines * lines * 10
        self.__lines_to_go -= lines
        if self.__lines_to_go <= 0:
            if self.__end_level:
                self.__end_level(level_no)
            self.__game.quit()
            if not self.load_level(self.__current_stage + 1):
                self.__game_completed = True
