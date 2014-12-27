#!/usr/bin/env python

import random
from beatbox import AUDIO

DEFAULT_PIECES = [
    [[1, 1],
     [1, 1]],

    [[2],
     [2],
     [2],
     [2]],

    [[0, 3, 3],
     [3, 3, 0]],

    [[4, 4, 0],
     [0, 4, 4]],

    [[5, 0],
     [5, 0],
     [5, 5]],

    [[0, 6],
     [0, 6],
     [6, 6]],

    [[0, 7, 0],
     [7, 7, 7]]
]

DEFAULT_SIZE = (10, 20)
DEFAULT_SPEED = 400

class Tetris(object):
    def __init__(self, size=DEFAULT_SIZE, speed=DEFAULT_SPEED,
                 pieces=DEFAULT_PIECES, callbacks={}):

        self.__game_speed = speed
        self.__current_speed = speed
        self.__current_tick = self.__current_speed

        self.__board = [[0 for i in range(size[0])] for j in range(size[1])]
        self.__board_size = size
        self.__pieces = pieces
        self.__next = self.any_piece
        self.__current = self.any_piece
        self.__current_position = (5 - (len(self.__current[0]) / 2), 0)
        self.__game_over = False

        self.__callbacks = callbacks

    @property
    def pieces(self):
        return self.__pieces

    @property
    def any_piece(self):
        return random.choice(self.__pieces)

    @property
    def game_over(self):
        return self.__game_over

    @property
    def next(self):
        return self.__next

    @property
    def board(self):
        return self.__board

    @property
    def player(self):
        return self.__current

    @property
    def player_position(self):
        return self.__current_position

    @property
    def size(self):
        return self.__board_size

    @property
    def speed(self):
        return self.__game_speed

    @property
    def CW_rotated_piece(self):
        return zip(*self.__current[::-1])

    @property
    def CCW_rotated_piece(self):
        return zip(*self.__current)[::-1]

    def piece_fit_in(self, piece, position):
        for y in range(len(piece)):
            for x in range(len(piece[y])):
                if piece[y][x]:
                    x_board = position[0] + x
                    y_board = position[1] + y
                    if ((x_board < 0) or (x_board >= self.__board_size[0]) or
                        (y_board < 0) or (y_board >= self.__board_size[1])):
                        return False
                    if self.__board[y_board][x_board]:
                        return False
        return True

    def current_piece_fit_in(self, position):
        return self.piece_fit_in(self.__current, position)

    def get_another_piece(self, drop=True):
        if drop:
            self.place_piece_cb()
            for y in range(len(self.__current)):
                for x in range(len(self.__current[y])):
                    if self.__current[y][x]:
                        x_board = self.__current_position[0] + x
                        y_board = self.__current_position[1] + y
                        self.__board[y_board][x_board] = self.__current[y][x]
        self.new_piece_cb()
        self.__current = self.__next
        self.__current_speed = self.__game_speed
        self.__next = self.any_piece
        self.__current_position = (5 - (len(self.__current[0]) / 2), 0)
        self.__game_over = not self.current_piece_fit_in(self.__current_position)

    def rotate_CW(self):
        if not self.piece_fit_in(self.CW_rotated_piece,
                                 self.__current_position):
            self.blocked_move_cb()
            return False
        self.__current = self.CW_rotated_piece
        self.move_cb()
        return True

    def rotate_CCW(self):
        if not self.piece_fit_in(self.CCW_rotated_piece,
                                 self.__current_position):
            self.blocked_move_cb()
            return False
        self.__current = self.CCW_rotated_piece
        self.move_cb()
        return True

    def move_left(self):
        if not self.current_piece_fit_in((self.__current_position[0] - 1,
                                          self.__current_position[1])):
            self.blocked_move_cb()
            return False
        self.__current_position = (self.__current_position[0] - 1,
                                   self.__current_position[1])
        self.move_cb()
        return True

    def move_right(self):
        if not self.current_piece_fit_in((self.__current_position[0] + 1,
                                          self.__current_position[1])):
            self.blocked_move_cb()
            return False
        self.__current_position = (self.__current_position[0] + 1,
                                   self.__current_position[1])
        self.move_cb()
        return True

    def move_down(self):
        if not self.current_piece_fit_in((self.__current_position[0],
                                          self.__current_position[1] + 1)):
            self.blocked_move_cb()
            return False
        self.__current_position = (self.__current_position[0],
                                   self.__current_position[1] + 1) 
        self.move_cb()
        return True

    def drop_piece(self):
        self.drop_piece_cb()
        self.__current_speed = 0

    def increase_speed(self, units=1):
        self.__game_speed -= units
        if self.__current_speed != 0:
            self.__current_speed = self.__game_speed

    def decrease_speed(self, units=1):
        self.__game_speed += units
        if self.__current_speed != 0:
            self.__current_speed = self.__game_speed

    @property
    def completed_rows(self):
        completed_rows = []
        for y in range(len(self.__board)):
            completed = True
            for x in range(len(self.__board[y])):
                if not self.__board[y][x]:
                    completed = False
                    break
            if completed:
                completed_rows.append(y)
        return completed_rows

    def remove_row(self, row):
        if row in range(self.__board_size[1]):
            rows_to_move = range(row + 1)
            rows_to_move.reverse()
            for y in rows_to_move[:-1]:
                for x in range(len(self.__board[row])):
                    self.__board[y][x] = self.__board[y - 1][x]
            for x in range(len(self.__board[0])):
                self.__board[0][x] = 0
            callback = self.__callbacks.get('row_clear', None)
            if callback:
                callback()
            return True
        return False

    def quit(self):
        self.__game_over = True
        
    def update(self):
        lines = 0

        if self.game_over:
            return lines

        self.__current_tick -= 1

        if self.__current_tick < 0:
            self.__current_tick = self.__current_speed
            if not self.move_down():
                self.get_another_piece()

                for row in self.completed_rows:
                    lines += 1
                    self.remove_row(row)

        return lines

    def set_callback(self, callback_id, callback):
        self.__callbacks[callback_id] = callback
        
    def new_piece_cb(self):
        callback = self.__callbacks.get('new_piece', None)
        if callback:
            callback()

    def drop_piece_cb(self):
        AUDIO.play_sound('drop')
        callback = self.__callbacks.get('drop_piece', None)
        if callback:
            callback()
        
    def place_piece_cb(self):
        callback = self.__callbacks.get('place_piece', None)
        if callback:
            callback()

    def blocked_move_cb(self):
        callback = self.__callbacks.get('blocked_move', None)
        if callback:
            callback()

    def move_cb(self):
        callback = self.__callbacks.get('move', None)
        if callback:
            callback()
