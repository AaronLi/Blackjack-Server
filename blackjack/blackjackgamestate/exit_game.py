from blackjack.blackjackgamestate import gamestate


class ExitGame(gamestate.GameState):

    @staticmethod
    def poll(game: "db.game.Game") -> str:
        return "GAME OVER"