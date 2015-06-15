#!/usr/bin/env python

import sys
import json
import pygame
import os.path
import platform

import modes

pygame.font.init()
FONT = pygame.font.Font(None, 36)

CONFIG_FILE = 'config.json'


class UnsupportedPlatfform(Exception):
    def __str__(self):
        return 'Unsupported platform: %s' % platform.system()


class MissingFile(Exception):
    def __init__(self, filename):
        self.__file = filename
    def __str__(self):
        return 'Required file not found: %s' % self.__file


def __resource_folder():
    system = platform.system()
    if system == 'Linux':
        return ['/usr/share/games/aftris',
                '/usr/local/share/games/aftris',
                os.path.join(os.getcwd(), 'res')]
    else:
        raise UnsupportedPlatform()

def __config_folder():
    system = platform.system()
    if system == 'Linux':
        return [os.path.join(os.path.expanduser('~'), '.aftris')]

def __get_file(filename, search_folders, required=True):
    for folder in search_folders:
        current_check_file = os.path.join(folder, filename)
        if os.path.isfile(current_check_file):
            return current_check_file
    if required:
        raise MissingFile(filename)


def init_config():
    config_file = os.path.join(__config_folder()[0], CONFIG_FILE)
    with open(config_file, 'w') as fd:
        json.dump(fd, {}, sort_keys=True, indent=4)
    return config_file

def load_config():
    config_file = __get_file(CONFIG_FILE, __config_folder(), required=False)
    if not config_file:
        config_file = init_config()
        return {}
    with open(config_file, 'r') as fd:
        return json.load(fd)

def save_config():
    config_file = __get_file(CONFIG_FILE, __config_folder(), required=False)
    if not config_file:
        config_file = init_config()
    with open(config_file, 'w') as fd:
        return json.load(fd)


def load_image(image_name):
    filename = __get_file(image_name, __resource_folder())
    surface = pygame.image.load(filename)
    # FIXME: check if display is initialized
    #        this is not mandatory
    # surface = surface.convert_alpha()
    return surface


def load_music(music_name):
    filename = __get_file(music_name, __resource_folder())
    return filename


def load_sound(sound_name):
    filename = __get_file(sound_name, __resource_folder())
    return pygame.mixer.Sound(filename)


# FIXME: https://github.com/int-0/aftris/issues/17
#
def load_level(level_filename):
    filename = __get_file(level_filename, __resource_folder())
    with open(filename, 'r') as fd:
        level = json.load(fd)
    level.update({
        'background': load_image(level['background'])
        })
    return modes.Stage(level)
