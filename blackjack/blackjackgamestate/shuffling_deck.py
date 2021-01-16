from blackjack.blackjackgamestate import gamestate, state
import db.game

class ShufflingDeck(gamestate.GameState):
    @staticmethod
    def enter(game: "db.game.Game") -> "db.game.Game":
        game.deck.shuffle_deck()
        game.change_state(state.State.INITIAL_MOVE)
        return game


    @staticmethod
    def poll(game: "db.game.Game") -> str:
        # shouldn't be called, shuffling should go straight to another state
        raise Exception("Illegal access")
        return game

    @staticmethod
    def input(game: "db.game.Game", action_code: str) -> "db.game.Game":
        raise Exception("Illegal access")
        return game

    @staticmethod
    def exit(game: "db.game.Game") -> "db.game.Game":
        return game