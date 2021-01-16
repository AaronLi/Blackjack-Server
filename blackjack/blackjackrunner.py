import logging

import pymodm

from db.game import Game
from blackjack.blackjackgamestate import dispatcher
from blackjack.blackjackgamestate import state
pymodm.connect(
    "mongodb+srv://dumfingDBAccessor:JT2EiypXUvcxZsh6@minelotto.qv8xb.mongodb.net/minelotto?retryWrites=true&w=majority")

game = Game()
game.save()
game_dispatcher = dispatcher.Dispatcher()

logging.getLogger(__name__).setLevel(logging.DEBUG)
while game.state != state.State.END:
    print(game_dispatcher.poll(game))
    u_in = input()
    current_game_state, response = game_dispatcher.input(game, u_in)
    current_game_state.save()