#!/usr/bin/env python

import time
import numpy
import pygame

def ShowImage(screen, image):
    center = screen.get_rect().center
    screen.blit(image,
                (center[0] - (image.get_rect().width / 2),
                 center[1] - (image.get_rect().height / 2)))
    pygame.display.flip()


def FadeTo(screen, source, destination, frames=20):
    size = source.get_size()
    center = screen.get_rect().center
    src = pygame.surfarray.pixels3d(source)
    dest = pygame.surfarray.pixels3d(destination)
    image = pygame.surfarray.pixels3d(pygame.Surface(size))
    
    columns = range(size[0])
    rows = range(size[1])

    for frame in range(frames + 1):
        fin = float(frame) / float(frames)
        fout = float(frames - frame) / float(frames)
        image = (src * fout) + (dest * fin)
        screen.blit(pygame.surfarray.make_surface(image),
                    (center[0] - (size[0] / 2),
                     center[1] - (size[1] / 2)))
        pygame.display.flip()


def ShowLogo(screen):
    clock = pygame.time.Clock()
    logo_frame = [
        pygame.image.load('res/int0_sketch.png'),
        pygame.image.load('res/int0_pencil.png'),
        pygame.image.load('res/int0_ink.png'),
        pygame.image.load('res/int0_final.png')
    ]
    white = pygame.Surface(logo_frame[0].get_size())
    white.fill((255, 255, 255, 255))

    black = pygame.Surface(screen.get_size())
    black = black.convert_alpha()
    black.set_alpha(255)
    black.fill((0, 0, 0, 0))

    screen.fill((0, 0, 0))
    pygame.display.flip()
    for w in range(256):
        screen.fill((w, w, w))
        pygame.display.flip()

    FadeTo(screen, white, logo_frame[0])
    for frm in range(len(logo_frame) -1):
        FadeTo(screen, logo_frame[frm], logo_frame[frm + 1])

    time.sleep(1.0)

    for w in range(256):
        black.fill((0, 0, 0, w))
        screen.blit(black, (0, 0))
        pygame.display.flip()
