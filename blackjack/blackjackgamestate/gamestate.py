from abc import ABC
from typing import Tuple

import db.game


class GameState(ABC):

    @staticmethod
    def enter(game: "db.game.Game") -> "db.game.Game":
        """
        Called when you enter the state
        :type game: blackjack.db.game.Game
        """
        return game

    @staticmethod
    def poll(game: "db.game.Game") -> str:
        """
        Called when a client wants to know what the state of the game is and what their actions are
        """
        return ""

    @staticmethod
    def input(game: "db.game.Game", action_code: str) -> Tuple["db.game.Game", str]:
        """
        Called when a client is interacting with the game,
        :param game the current game state
        :param action_code the action the client wishes to perform
        :returns the new state of the game and a string to respond to the client with
        """
        return game, ""

    @staticmethod
    def exit(game: "db.game.Game") -> "db.game.Game":
        """
        Called when a state is being transitioned out of
        """
        return game