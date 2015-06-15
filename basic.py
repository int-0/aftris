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
