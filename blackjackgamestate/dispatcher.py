from typing import Sequence, Tuple

from blackjackgamestate import gamestate, dealer_move, payout, continue_playing, exit_game, state, setting_bet, \
    shuffling_deck, initial_move, player_move


class Dispatcher(gamestate.GameState):
    @staticmethod
    def dispatch(game_state: state.State):
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
    def enter(game: "BlackJackGame") -> "BlackJackGame":
        return Dispatcher.dispatch(game.state).enter(game)

    @staticmethod
    def poll(game: "BlackJackGame") -> str:
        return Dispatcher.dispatch(game.state).poll(game)

    @staticmethod
    def input(game: "BlackJackGame", action_code: str) -> Tuple["BlackJackGame", str]:
        return Dispatcher.dispatch(game.state).input(game, action_code)

    @staticmethod
    def exit(game: "BlackJackGame") -> "BlackJackGame":
        return Dispatcher.dispatch(game.state).exit(game)

