import logging
from datetime import datetime
from typing import Tuple
import db.game
from blackjack.blackjackgamestate import payout, continue_playing, exit_game, setting_bet, \
    shuffling_deck, initial_move, player_move
from blackjack.blackjackgamestate import gamestate, state, dealer_move


class Dispatcher(gamestate.GameState):
    @staticmethod
    def dispatch(game_state: int):
        logging.debug(f"Current state {state.State(game_state).name}")
        if game_state == state.State.SETTING_BET:
            return setting_bet.SetBet
        elif game_state == state.State.SHUFFLING_DECK:
            return shuffling_deck.ShufflingDeck
        elif game_state == state.State.INITIAL_MOVE:
            return initial_move.InitialMove
        elif game_state == state.State.PLAYER_MOVE:
            return player_move.PlayerMove
        elif game_state == state.State.DEALER_MOVE:
            return dealer_move.DealerMove
        elif game_state == state.State.PAYOUT:
            return payout.Payout
        elif game_state == state.State.CONTINUE_PLAYING:
            return continue_playing.ContinuePlaying
        elif game_state == state.State.END:
            return exit_game.ExitGame

    @staticmethod
    def enter(game: "db.game.Game") -> "db.game.Game":
        return Dispatcher.dispatch(game.state).enter(game)

    @staticmethod
    def poll(game: "db.game.Game") -> str:
        return Dispatcher.dispatch(game.state).poll(game)

    @staticmethod
    def input(game: "db.game.Game", action_code: str) -> Tuple["db.game.Game", str]:
        game.last_move_time = datetime.now()
        return Dispatcher.dispatch(game.state).input(game, action_code)

    @staticmethod
    def exit(game: "db.game.Game") -> "db.game.Game":
        return Dispatcher.dispatch(game.state).exit(game)

