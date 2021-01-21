import typing
import db.game
from blackjack.blackjackgamestate import gamestate, state, dispatcher


class ContinuePlaying(gamestate.GameState):
    @staticmethod
    def enter(game: "db.game.Game") -> "db.game.Game":
        return super(ContinuePlaying, ContinuePlaying).enter(game)

    @staticmethod
    def poll(game: "db.game.Game") -> str:
        return "\n".join(("continueplaying", str(game), "moves 2 "+ " ".join(ContinuePlaying.get_valid_moves(game))))

    @staticmethod
    def input(game: "db.game.Game", action_code: str) -> typing.Tuple["db.game.Game", str]:
        if action_code in ContinuePlaying.get_valid_moves(game):
            if action_code == "yes":
                if game.player.balance < sum(hand.bet for hand in game.player_hands):
                    game.setup_new_round()
                    game.change_state(state.State.SETTING_BET)
                elif len(game.deck.cards) < game.deck.shuffle_point:
                    game.change_state(state.State.SHUFFLING_DECK)
                else:
                    game.change_state(state.State.INITIAL_MOVE)
            elif action_code == "no":
                game.change_state(state.State.END)
        return game, dispatcher.Dispatcher.poll(game)

    @staticmethod
    def exit(game: "db.game.Game") -> "db.game.Game":
        return super(ContinuePlaying, ContinuePlaying).exit(game)

    @staticmethod
    def get_valid_moves(game: "db.game.Game") -> typing.Sequence[str]:
        return "yes", "no"
