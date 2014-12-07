#!/usr/bin/env python

import pygame
from pygame.locals import color

import basic as theme

class Render(object):
    def __init__(self, game):
        self.__game = game

        scr_size = (self.__game.size[0] * theme.BRICK_SIZE + 4,
                    self.__game.size[1] * theme.BRICK_SIZE + 4)
        self.__scr = pygame.Surface(scr_size)
        self.__scr.fill(color.THECOLORS['white'])

        board_size = (self.__game.size[0] * theme.BRICK_SIZE,
                      self.__game.size[1] * theme.BRICK_SIZE)
        self.__board = pygame.Surface(board_size)
        self.__board.fill(color.THECOLORS['black'])

        self.__next = pygame.Surface((theme.BRICK_SIZE * 4,
                                      theme.BRICK_SIZE * 4))
        self.__next.fill(color.THECOLORS['black'])

    @property
    def surface(self):
        self.__scr.blit(self.__board, (2, 2))
        return self.__scr

    @property
    def next(self):
        return self.__next

    def score(self, score):
        return theme.FONT.render('%04d' % score, 1,
                                 (255, 255, 255, 255),
                                 (0, 0, 0, 255))

    def update(self):
        for y in range(len(self.__game.board)):
            for x in range(len(self.__game.board[y])):
                brick = theme.BRICKS.get(self.__game.board[y][x], None)
                if not brick:
                    continue
                self.__board.blit(brick, (x * theme.BRICK_SIZE,
                                          y * theme.BRICK_SIZE))

        self.__next.fill(color.THECOLORS['black'])
        for y in range(len(self.__game.next)):
            for x in range(len(self.__game.next[y])):
                brick = theme.BRICKS.get(self.__game.next[y][x], None)
                if not brick:
                    continue
                self.__next.blit(brick, (x * theme.BRICK_SIZE,
                                         y * theme.BRICK_SIZE))

        for y in range(len(self.__game.player)):
            for x in range(len(self.__game.player[y])):
                if not self.__game.player[y][x]:
                    continue
                brick = theme.BRICKS.get(self.__game.player[y][x], None)
                if not brick:
                    continue
                self.__board.blit(brick,
                                  ((x + self.__game.player_position[0]) * theme.BRICK_SIZE,
                                   (y + self.__game.player_position[1]) * theme.BRICK_SIZE))
        return self.surface
