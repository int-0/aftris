#!/usr/bin/env python

import time
import numpy
import pygame

import resources

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
        resources.load_image('int0_sketch.png'),
        resources.load_image('int0_pencil.png'),
        resources.load_image('int0_ink.png'),
        resources.load_image('int0_final.png')
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


def StartLevel(screen, background, level_no):
    size = resources.FONT.size('Level %s' % level_no)
    screen_size = screen.get_size()
    center = ((screen_size[0] / 2) - (size[0] / 2),
              (screen_size[1] / 2) - (size[1] / 2))
    for alpha in range(255):
        screen.blit(background, (0, 0))
        level = resources.FONT.render('Level %s' % level_no, 1,
                                      (alpha, alpha, alpha, 255))
        screen.blit(level, center)
        pygame.display.flip()
    time.sleep(1.0)
    
    for alpha in range(255):
        screen.blit(background, (0, 0))
        level = resources.FONT.render('Level %s' % level_no, 1,
                                      (255 - alpha, 255 - alpha, 255 -alpha, 255))
        screen.blit(level, center)
        pygame.display.flip()

    screen.blit(background, (0, 0))
    pygame.display.flip()
