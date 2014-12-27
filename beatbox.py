#!/usr/bin/env python

import pygame

from tools import singleton

@singleton
class Audio(object):
    def __init__(self, initial_musics={}, initial_sounds={}):
        if pygame.mixer.get_init() is None:
            pygame.mixer.init()
        self.__mute = False
        
        self.__sounds = initial_sounds
        self.__musics = initial_musics

    def register_sound(self, sound_id, sound_object):
        self.__sounds[sound_id] = sound_object

    def register_music(self, music_id, music_object):
        self.__musics[music_id] = music_object

    def unregister_sound(self, sound_id):
        if sound_id not in self.__sounds.keys():
            return False
        del(self.__sounds[sound_id])

    def unregister_music(self, music_id):
        if music_id not in self.__musics.keys():
            return False
        del(self.__musics[music_id])

    @property
    def sounds(self):
        return self.__sounds.keys()

    @property
    def musics(self):
        return self.__musics.keys()
    
    @property
    def is_muted(self):
        return self.__mute

    def mute(self):
        if self.is_muted:
            return
        pygame.mixer.music.stop()
        self.__mute = True

    def unmute(self):
        if not self.is_muted:
            return
        pygame.mixer.music.play(-1)

    def set_mute(self, new_state=True):
        if new_state:
            self.mute()
        else:
            self.unmute()

    def set_bgm_music(self, music_id):
        if music_id not in self.musics:
            return False
        pygame.mixer.music.load(self.__musics[music_id])
        if not self.is_muted:
            pygame.mixer.music.play(-1)
        return False
    
    def play_sound(self, sound_id):
        if self.is_muted:
            return True
        if sound_id not in self.sounds:
            return False
        self.__sounds[sound_id].play()
        return True

# Create default instance
AUDIO = Audio()
