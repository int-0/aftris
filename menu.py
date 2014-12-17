#!/usr/bin/env python

import time
import pygame
from cuts import FadeTo

import resources

class Menu(object):
    def __init__(self, screen, options=[], tile=None, background=None):
        self.__scr = screen
        self.__center = self.__scr.get_rect().center

        self.__options = []
        for option in options:
            self.__options.append(resources.FONT.render(option, 1,
                                                        (255, 255, 255, 255)))

        self.__tile = tile
        if self.__tile:
            self.__tile_center = (
                (self.__scr.get_width() / 2) - (self.__tile.get_width() / 2),
                (self.__tile.get_height() / 2))
        else:
            self.__tile_center = None

        if background:
            self.__gnd = background
        else:
            self.__gnd = pygame.Surface(self.__scr.get_size())
            self.__gnd.fill((0, 0, 0, 255))

        self.__selected = 0
        self.__selected_option = self.__options[self.__selected].copy()
        self.__dir = .005
        self.__zoom = 1.0

        self.__cancelled = False

    @property
    def options(self):
        return self.__options

    @property
    def selected(self):
        return self.__selected

    @property
    def cancelled(self):
        return self.__cancelled

    def add_option(self, option):
        self.__options.append(resources.FONT.render(option, 1,
                                                    (255, 255, 255, 255)))

    def select(self, option):
        self.__dir = .005
        self.__zoom = 1.0
        if option < 0:
            option = option + len(self.__options)
        self.__selected = option % len(self.__options)
        self.__selected_option = self.__options[self.__selected].copy()

    def __tile_animation(self):
        if self.__tile:
            self.__scr.blit(self.__tile, self.__tile_center)
        
    def __draw(self):
        self.__scr.blit(self.__gnd, (0, 0))
        self.__tile_animation()
        opno = 0
        for option in self.__options:
            y = option.get_size()[1]
            if opno == self.selected:
                self.__zoom += self.__dir
                if (self.__zoom >= 1.4) or (self.__zoom <= 1.0):
                    self.__dir = -self.__dir
                option = pygame.transform.rotozoom(option, 0,
                                                   self.__zoom)
            size = option.get_size()
            self.__scr.blit(option,
                            (self.__center[0] - (size[0] / 2),
                             self.__center[1] + int(1.25 * opno * y)))
            opno += 1

    def run(self):
        black = pygame.Surface(self.__scr.get_size())
        black.fill((0, 0, 0, 255))
        
        FadeTo(self.__scr, black, self.__gnd)
               
        select = False
        while not select:
            self.__draw()
            pygame.display.flip()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.select(self.selected + 1)
                    elif event.key == pygame.K_UP:
                        self.select(self.selected - 1)
                    elif event.key in [pygame.K_SPACE,
                                       pygame.K_ESCAPE,
                                       pygame.K_RETURN]:
                        self.__cancelled = event.key == pygame.K_ESCAPE
                        select = True
