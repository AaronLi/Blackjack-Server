from blackjack.blackjackgamestate import dispatcher
from blackjack.blackjackgamestate import gamestate, state
from blackjack import MAX_BET, BET_SIZES
from db import user


class SetBet(gamestate.GameState):
    @staticmethod
    def enter(game):
        game.player_hands[0].bet = 0

    @staticmethod
    def poll(game) -> str:
        move_options = SetBet.get_possible_moves(game).keys()
        # current bet, options, move list
        return f"betting {game.player_hands[0].bet}\nmoves {len(move_options)} {' '.join(move_options)}"

    @staticmethod
    def input(game: "BlackJackGame", action_code):
        possible_moves = SetBet.get_possible_moves(game)
        if action_code not in possible_moves:
            pass
        elif action_code == "submitbet":
            game.change_state(state.State.SHUFFLING_DECK)
        else:
            game.player_hands[0].bet += possible_moves[action_code]
        return game, dispatcher.Dispatcher.poll(game)

    @staticmethod
    def exit(game):
        game.player.balance -= game.player_hands[0].bet
        game.player.save()
        print(repr(user.User.objects.get({"_id":game.player.username})))

    @staticmethod
    def get_possible_moves(game):
        options = {}
        if game.player_hands[0].bet > 0:
            options["submitbet"] = 0
        for bet_size in BET_SIZES:
            if game.player_hands[0].bet >= bet_size:
                options[f"bet-{bet_size}"] = -bet_size
            if (game.player_hands[0].bet <= MAX_BET - bet_size) and game.player.balance >= (game.player_hands[0].bet + bet_size):
                options[f"bet{bet_size}"] = bet_size
        return options
