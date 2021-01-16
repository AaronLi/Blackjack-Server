from blackjack.blackjackgamestate import gamestate


class ExitGame(gamestate.GameState):

    @staticmethod
    def poll(game: "db.game.Game") -> str:
        game.player.current_game.delete()
        return "GAME OVER"