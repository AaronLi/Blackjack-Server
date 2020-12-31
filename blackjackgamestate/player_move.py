import collections
import enum
import typing

from blackjackgamestate import gamestate, state, dispatcher
import hand_state


class PlayerMove(gamestate.GameState):
    class PlayerAction(enum.Enum):
        HIT = 0
        STAND = 1

    ActionPair = collections.namedtuple("ActionPair", ("action_code", "hand"))

    @staticmethod
    def enter(game: "BlackJackGame") -> "BlackJackGame":
        # 
        return super(PlayerMove, PlayerMove).enter(game)

    @staticmethod
    def poll(game: "BlackJackGame") -> str:

        valid_moves = PlayerMove.get_possible_moves(game).keys()
        # string for section, number of codes, list of codes
        valid_moves_string = f"moves {len(valid_moves)} {' '.join(valid_moves)}"
        return '\n'.join(("playermove", str(game), valid_moves_string))


    @staticmethod
    def input(game: "BlackJackGame", action_code: str) -> typing.Tuple["BlackJackGame", str]:
        """
        Handle Player Input
        :param game: The current game state
        :param action_code: The action to take
        :return: The game object and a string representing the new state of the game
        """
        valid_moves = PlayerMove.get_possible_moves(game)
        action = valid_moves.get(action_code)
        if action is None:
            return game, PlayerMove.poll(game)

        if action.action_code == PlayerMove.PlayerAction.HIT:
            drawn_card = game.deck.draw_card()
            game.player_hands[action.hand].cards.append(drawn_card)

            if len(PlayerMove.get_possible_moves(game)) == 0:
                # no possible moves remain
                game.change_state(state.State.DEALER_MOVE)

        elif action.action_code == PlayerMove.PlayerAction.STAND:
            game.player_hands[action.hand].hand_state |= hand_state.HandState.STANDING

            if len(PlayerMove.get_possible_moves(game)) == 0:
                # no possible moves remain
                game.change_state(state.State.DEALER_MOVE)

        return game, dispatcher.Dispatcher.poll(game)

    @staticmethod
    def exit(game: "BlackJackGame") -> "BlackJackGame":
        return super(PlayerMove, PlayerMove).exit(game)

    @staticmethod
    def get_possible_moves(game: "BlackJackGame") -> typing.MutableMapping[str, ActionPair]:
        """
        Get the possible actions a player can make
        :param game: The current state of the game
        :return: A mapping from action code to action and hand index pairs
        """
        options = {}

        for i, player_hand in enumerate(game.player_hands):
            if player_hand.hand_state == hand_state.HandState.INACTIVE:
                # inactive
                print(f"hand {i} inactive")
                continue

            if player_hand.hand_state & hand_state.HandState.STANDING:
                # hand is standing
                print(f"hand {i} standing")
                continue

            is_busted = all(score > 21 for score in game.get_hand_scores(i))
            if is_busted:
                # hand is busted
                print(f"hand {i} busted")
                continue

            print(f"hand {i} able")
            options.update({
                f"hit_{i}": PlayerMove.ActionPair(PlayerMove.PlayerAction.HIT, i),
                f"stand_{i}": PlayerMove.ActionPair(PlayerMove.PlayerAction.STAND, i)
            })
            break
        return options
