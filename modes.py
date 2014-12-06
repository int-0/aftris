#!/usr/bin/env python

import game
import pygame

LINES_TO_SPEED_UP = 10

BACKGROUNDS = [
    pygame.image.load('res/ingamegnd.png'),
    pygame.image.load('res/ingamegnd2.png')
]

LINES_TO_CYCLE = 19


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


class Mode(object):
    def __init__(self,
                 board_size=game.DEFAULT_SIZE,
                 initial_speed=game.DEFAULT_SPEED,
                 callbacks={}):
        self.__game = game.Tetris(board_size, initial_speed)
        self.__last_completed = 0
        self.__lines = 0
        
    @property
    def show_next(self):
        return False

    @property
    def game(self):
        return self.__game

    def set_game(self, game):
        self.__game = game
        
    @property
    def game_over(self):
        return self.__game.game_over

    @property
    def score(self):
        return 0

    @property
    def lines(self):
        return self.__lines

    @property
    def last_lines_completed(self):
        return self.__last_completed
    
    @property
    def completed(self):
        return False

    def update(self):
        self.__last_completed = self.game.update()
        self.__lines += self.__last_completed


class Forever(Mode):
    def __init__(self, size=game.DEFAULT_SIZE,
                 initial_speed=game.DEFAULT_SPEED,
                 callbacks=None):
        Mode.__init__(self, size, initial_speed, callbacks)

        self.__score = 0

        self.__change_background = callbacks.get('change_background', None)
        self.__current_background = 0
        self.__lines_to_cycle = LINES_TO_CYCLE
        
        self.__lines_to_speed_up = LINES_TO_SPEED_UP

    @property
    def show_next(self):
        return True

    @property
    def score(self):
        return self.__score

    def cycle_background(self):
        if self.__change_background is not None:
            self.__current_background += 1
            self.__current_background %= len(BACKGROUNDS)
            self.__change_background(BACKGROUNDS[self.__current_background])
        
    def update(self):
        Mode.update(self)
        self.__score += (pow(self.last_lines_completed, 2) * 10)
        self.__lines_to_speed_up -= self.last_lines_completed
        if self.__lines_to_speed_up < 0:
            self.__lines_to_speed_up = LINES_TO_SPEED_UP
            self.game.increase_speed(10)

        self.__lines_to_cycle -= self.last_lines_completed
        if self.__lines_to_cycle < 0:
            self.__lines_to_cycle = LINES_TO_CYCLE
            self.cycle_background()


class Levels(Mode):
    def __init__(self, size=game.DEFAULT_SIZE,
                 initial_speed=game.DEFAULT_SPEED,
                 stages=[],
                 callbacks=None):
        Mode.__init__(self, size, initial_speed, callbacks)

        self.__score = 0

        self.__lines_to_go = 0
        self.__current_stage = 0
        self.__show_next = True
        self.__stages = stages
        self.__game_completed = False

        self.__start_level_cb = callbacks.get('start_level', None)
        self.__end_level_cb = callbacks.get('end_level', None)
        self.__change_background = callbacks.get('change_background', None)
        self.load_level(self.__current_stage)

    @property
    def show_next(self):
        return self.__show_next

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
        self.set_game(game.Tetris(self.game.size, new_speed))
        for position, block in level.extra_blocks:
            self.game.board[position[1]][position[0]] = block
        self.__show_next = level.show_next
        self.__lines_to_go = level.lines_to_go
        if level.background:
            self.__set_background(level.background)
        if self.__start_level:
            self.__start_level(level_no)
        return True

    def update(self):
        if self.completed:
            return
        Mode.update(self)
        self.__score += (pow(self.last_lines_completed, 2) * 10)
        self.__lines_to_go -= self.last_lines_completed
        if self.__lines_to_go <= 0:
            if self.__end_level:
                self.__end_level(level_no)
            self.game.quit()
            if not self.load_level(self.__current_stage + 1):
                self.__game_completed = True

    def __set_background(self, background):
        if self.__set_background is not None:
            self.__change_background(background)

    def __start_level(self, level_number):
        if self.__start_level_cb is not None:
            self.__start_level_cb(level_number)

    def __end_level(self, level_number):
        if self.__end_level_cb is not None:
            self.__end_level_cb(level_number)
            
