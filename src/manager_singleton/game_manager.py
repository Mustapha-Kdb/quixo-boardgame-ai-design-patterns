import pygame
from model.board import Board
from model.human_player import HumanPlayer

class GameManager:

    __instance = None

    # implementation of singleton
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    # constructeur
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.current_state = None
            self.screen = None
            self.clock = None
            self.board = Board()

            # init players
            self.players = [
                HumanPlayer(symbol='X'),
                HumanPlayer(symbol='O')
            ]
            self.current_player_index = 0

    def set_state(self, state):
        self.current_state = state

    def get_state(self):
        return self.current_state

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        return self.players[self.current_player_index]

    def get_current_player(self):
        return self.players[self.current_player_index]
