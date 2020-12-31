import typing

from blackjackgamestate import gamestate, state


class ContinuePlaying(gamestate.GameState):
    @staticmethod
    def enter(game: "BlackJackGame") -> "BlackJackGame":
        return super(ContinuePlaying, ContinuePlaying).enter(game)

    @staticmethod
    def poll(game: "BlackJackGame") -> str:
        return "\n".join(("continueplaying", str(game), " ".join(ContinuePlaying.get_valid_moves(game))))

    @staticmethod
    def input(game: "BlackJackGame", action_code: str) -> typing.Tuple["BlackJackGame", str]:
        if action_code in ContinuePlaying.get_valid_moves(game):
            if action_code == "yes":
                if len(game.deck) < game.deck.shuffle_point:
                    game.change_state(state.State.SHUFFLING_DECK)
                else:
                    game.change_state(state.State.INITIAL_MOVE)
            elif action_code == "no":
                game.change_state(state.State.END)
        return super(ContinuePlaying, ContinuePlaying).input(game, action_code)

    @staticmethod
    def exit(game: "BlackJackGame") -> "BlackJackGame":
        return super(ContinuePlaying, ContinuePlaying).exit(game)

    @staticmethod
    def get_valid_moves(game: "BlackJackGame") -> typing.Sequence[str]:
        return "yes", "no"