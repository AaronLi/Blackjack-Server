from blackjackgamestate import gamestate, state


class ShufflingDeck(gamestate.GameState):
    @staticmethod
    def enter(game: "BlackJackGame") -> "BlackJackGame":
        game.deck.shuffle_deck()
        game.change_state(state.State.INITIAL_MOVE)
        return game


    @staticmethod
    def poll(game: "BlackJackGame") -> str:
        # shouldn't be called, shuffling should go straight to another state
        raise Exception("Illegal access")
        return game

    @staticmethod
    def input(game: "BlackJackGame", action_code: str) -> "BlackJackGame":
        raise Exception("Illegal access")
        return game

    @staticmethod
    def exit(game: "BlackJackGame") -> "BlackJackGame":
        return game