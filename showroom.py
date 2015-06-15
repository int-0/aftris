#!/usr/bin/env python

import pygame
import threading

DEFAULT_RESOLUTION = (640, 480)
DEFAULT_FPS = 90

class Element(object):
    def __init__(self, frames=[], loop=False, kill_cb=None):
        self.__frames = frames
        self.__length = len(self.__frames)
        self.__kill_cb = kill_cb
        if loop:
            self.next_frame = self.__next_looping
        else:
            self.next_frame = self.__next_onedir
        
    @property
    def frame(self):
        return self.__frames

    def __next_looping(self, current_frame):
        return (current_frame + 1) % self.__length

    def __next_onedir(self, current_frame):
        if current_frame >= self.__length:
            return None
        return current_frame + 1

    def kill_cb(self):
        if not self.__kill_cb:
            return
        self.__kill_cb()
        

class ShowRoom(object):
    def __init__(self, update_cb=None):
        self.__scr = pygame.display.get_surface()

        self.__active = True
        self.__elements = {}
        self.__econfig = {}
        self.__dirty = []
        
        self.__update_callback = update_cb
        self.__current_fps = DEFAULT_FPS

    @property
    def elements(self):
        return self.__elements.keys()

    @property
    def active(self):
        return self.__active

    def set_update_cb(self, update_cb):
        self.__update_callback = update_cb
        
    def blit(self, overlay, position):
        self.__dirty.append(self.__scr.blit(overlay, position))
        
    def add_element(self, element_id, element, position):
        self.__elements[element_id] = element
        self.__econfig[element_id] = (position, 0)

    def move_element(self, element_id, position):
        if element_id not in self.elements:
            return False
        self.__econfig[element_id] = (position,
                                      self.__econfig[element_id][1])
        return True
        
    def restart_element(self, element_id):
        if element_id not in self.elements:
            return False
        self.__econfig[element_id] = (self.__econfig[element_id][0], 0)
        return True
    
    def set_fps(self, fps):
        self.__current_fps = fps

    def stop(self):
        self.__active = False
        
    def render(self):
        # Compute frame
        kill = []

        # Draw each element
        for element in self.elements:
            frame = self.__elements[element].frame[self.__econfig[element][1]]
            next_frm = self.__elements[element].next_frame(
                self.__econfig[element][1])
            if not next_frm:
                kill.append(element)
            else:
                self.__econfig[element] = (self.__econfig[element][0], next_frm)
            self.__dirty.append(
                self.__scr.blit(frame, self.__econfig[element][0]))

        # Update screen
        pygame.display.update(self.__dirty)
        self.__dirty = []

        # Remove dead elements
        for dead_element in kill:
            self.__elements[dead_element].kill_cb()
            del(self.__elements[dead_element])
            del(self.__econfig[dead_element])

    def loop(self):
        while self.__active:
            self.render()
            # Update game
            if self.__update_callback:
                self.__update_callback()
            # Control FPS
            pygame.time.Clock().tick(self.__current_fps)
