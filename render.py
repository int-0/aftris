#!/usr/bin/env python

import pygame
from pygame.locals import color

BRICK_SIZE = 20

BRICKS = {
    0: pygame.Surface((BRICK_SIZE, BRICK_SIZE)),
    1: pygame.Surface((BRICK_SIZE, BRICK_SIZE)),
    2: pygame.Surface((BRICK_SIZE, BRICK_SIZE)),
    3: pygame.Surface((BRICK_SIZE, BRICK_SIZE)),
    4: pygame.Surface((BRICK_SIZE, BRICK_SIZE)),
    5: pygame.Surface((BRICK_SIZE, BRICK_SIZE)),
    6: pygame.Surface((BRICK_SIZE, BRICK_SIZE)),
    7: pygame.Surface((BRICK_SIZE, BRICK_SIZE))
}

BRICKS[0].fill(color.THECOLORS['black'])
BRICKS[1].fill(color.THECOLORS['steelblue'])
pygame.draw.rect(BRICKS[1], (45, 65, 90, 255), BRICKS[1].get_rect(), 1)
BRICKS[2].fill(color.THECOLORS['red'])
pygame.draw.rect(BRICKS[2], (128, 0, 0, 255), BRICKS[2].get_rect(), 1)
BRICKS[3].fill(color.THECOLORS['lightblue'])
pygame.draw.rect(BRICKS[3], (86, 108, 115, 255), BRICKS[3].get_rect(), 1)
BRICKS[4].fill(color.THECOLORS['orange'])
pygame.draw.rect(BRICKS[4], (127, 182, 0, 255), BRICKS[4].get_rect(), 1)
BRICKS[5].fill(color.THECOLORS['pink'])
pygame.draw.rect(BRICKS[5], (127, 96, 101, 255), BRICKS[5].get_rect(), 1)
BRICKS[6].fill(color.THECOLORS['yellow'])
pygame.draw.rect(BRICKS[6], (127, 127, 0, 255), BRICKS[6].get_rect(), 1)
BRICKS[7].fill(color.THECOLORS['green'])
pygame.draw.rect(BRICKS[7], (0, 127, 0, 255), BRICKS[7].get_rect(), 1)

pygame.font.init()
FONT = pygame.font.Font(None, 36)

class Render(object):
    def __init__(self, game):
        self.__mode = game
        self.__game = self.__mode.game

        scr_size = (self.__game.size[0] * BRICK_SIZE + 4,
                    self.__game.size[1] * BRICK_SIZE + 4)
        self.__scr = pygame.Surface(scr_size)
        self.__scr.fill(color.THECOLORS['white'])

        board_size = (self.__game.size[0] * BRICK_SIZE,
                      self.__game.size[1] * BRICK_SIZE)
        self.__board = pygame.Surface(board_size)
        self.__board.fill(color.THECOLORS['black'])

        self.__next = pygame.Surface((BRICK_SIZE * 4, BRICK_SIZE * 4))
        self.__next.fill(color.THECOLORS['black'])

    @property
    def surface(self):
        self.__scr.blit(self.__board, (2, 2))
        return self.__scr

    @property
    def next(self):
        return self.__next

    @property
    def score(self):
        return FONT.render('%04d' % self.__mode.score, 1,
                           (255, 255, 255, 255),
                           (0, 0, 0, 255))

    def update(self):
        for y in range(len(self.__game.board)):
            for x in range(len(self.__game.board[y])):
                brick = BRICKS.get(self.__game.board[y][x], None)
                if not brick:
                    continue
                self.__board.blit(brick, (x * BRICK_SIZE,
                                          y * BRICK_SIZE))

        self.__next.fill(color.THECOLORS['black'])
        for y in range(len(self.__game.next)):
            for x in range(len(self.__game.next[y])):
                brick = BRICKS.get(self.__game.next[y][x], None)
                if not brick:
                    continue
                self.__next.blit(brick, (x * BRICK_SIZE, y * BRICK_SIZE))

        for y in range(len(self.__game.player)):
            for x in range(len(self.__game.player[y])):
                if not self.__game.player[y][x]:
                    continue
                brick = BRICKS.get(self.__game.player[y][x], None)
                if not brick:
                    continue
                self.__board.blit(brick,
                                  ((x + self.__game.player_position[0]) * BRICK_SIZE,
                                   (y + self.__game.player_position[1]) * BRICK_SIZE))
        return self.surface
