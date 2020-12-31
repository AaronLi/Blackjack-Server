import enum
from abc import ABC
from typing import Sequence, Tuple


class GameState(ABC):

    @staticmethod
    def enter(game: "BlackJackGame") -> "BlackJackGame":
        """
        Called when you enter the state
        :type game: blackjack.BlackJackGame
        """
        return game

    @staticmethod
    def poll(game: "BlackJackGame") -> str:
        """
        Called when a client wants to know what the state of the game is and what their actions are
        """
        return ""

    @staticmethod
    def input(game: "BlackJackGame", action_code: str) -> Tuple["BlackJackGame", str]:
        """
        Called when a client is interacting with the game,
        :param game the current game state
        :param action_code the action the client wishes to perform
        :returns the new state of the game and a string to respond to the client with
        """
        return game, ""

    @staticmethod
    def exit(game: "BlackJackGame") -> "BlackJackGame":
        """
        Called when a state is being transitioned out of
        """
        return game