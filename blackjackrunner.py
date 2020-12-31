import blackjack
from blackjackgamestate import dispatcher, state

game = blackjack.BlackJackGame()
game_dispatcher = dispatcher.Dispatcher()

while game.state != state.State.END:
    print(game_dispatcher.poll(game))
    u_in = input()
    game_dispatcher.input(game, u_in)