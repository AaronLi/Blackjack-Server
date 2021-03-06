import enum
import typing
import db.game
from blackjack import hand_state, blackjackcard
from blackjack.blackjackgamestate import player_move, dispatcher
from blackjack.blackjackgamestate import state


class InitialMove(player_move.PlayerMove):
    class PlayerActionInitial(enum.Enum):
        HIT = 0
        STAND = 1
        SPLIT = 2
        DOUBLE = 3

    @staticmethod
    def enter(game: "db.game.Game") -> "db.game.Game":

        game.player.balance -= game.player_hands[0].bet
        game.player.save()

        game.setup_new_round()

        # draw 2 cards for each player, alternating between player and dealer
        game.player_hands[0].cards.append(game.deck.draw_card())
        game.dealer_hand.cards.append(game.deck.draw_card())
        game.player_hands[0].cards.append(game.deck.draw_card())
        game.dealer_hand.cards.append(game.deck.draw_card())

        game.player_natural = 21 in game.get_hand_scores(0)
        game.dealer_natural = 21 in game.get_hand_scores(-1)
        if game.player_natural or game.dealer_natural:
            game.change_state(state.State.DEALER_MOVE)

        return super(InitialMove, InitialMove).enter(game)

    @staticmethod
    def poll(game: "db.game.Game") -> str:
        valid_moves = InitialMove.get_possible_moves(game).keys()
        valid_moves_string = f"moves {len(valid_moves)} {' '.join(valid_moves)}"
        return '\n'.join(('playermove', str(game), valid_moves_string))

    @staticmethod
    def input(game: "db.game.Game", action_code: str) -> typing.Tuple["db.game.Game", str]:
        valid_moves = InitialMove.get_possible_moves(game)
        action_pair = valid_moves.get(action_code)

        if action_pair is None:
            return game, dispatcher.Dispatcher.poll(game)

        if action_pair.action_code == InitialMove.PlayerActionInitial.DOUBLE:
            # Doubling down draws a card to the hand and stands
            drawn_card = game.deck.draw_card()
            game.player_hands[action_pair.hand].hand_state |= hand_state.HandState.DOUBLING
            game.player_hands[action_pair.hand].hand_state |= hand_state.HandState.STANDING
            game.player_hands[action_pair.hand].cards.append(drawn_card)
            game.player.balance -= game.player_hands[action_pair.hand].bet # deduct bet amount again for doubled bet
            game.player.save()

            if len(InitialMove.get_possible_moves(game)) == 0:
                game.change_state(state.State.DEALER_MOVE)
        elif action_pair.action_code == InitialMove.PlayerActionInitial.SPLIT:
            game.player_hands[1].hand_state |= hand_state.HandState.ACTIVE
            game.player_hands[1].cards.append(game.player_hands[0].cards.pop())
            game.player_hands[1].bet = game.player_hands[0].bet
            # now do initial move again for each hand
        else:
            return super(InitialMove, InitialMove).input(game, action_code)



        return game, dispatcher.Dispatcher.poll(game)

    @staticmethod
    def exit(game: "db.game.Game") -> "db.game.Game":
        return super(InitialMove, InitialMove).exit(game)

    @staticmethod
    def get_possible_moves(game: "db.game.Game") -> typing.MutableMapping[str, player_move.PlayerMove.ActionPair]:
        """
        Gets the possible moves for an initial move,
        these are identical to a normal move except you can split your hand or double your bet
        assumptions:
        there are only 2 cards and 1 hand
        there are 2 hands with 1 card
        :param game:
        :return:
        """

        possible_moves = {}

        num_active_hands = len(tuple(hand for hand in game.player_hands if hand.hand_state & hand_state.HandState.ACTIVE))
        for i, hand in enumerate(game.player_hands):
            if hand.hand_state & hand_state.HandState.STANDING:
                continue

            if not (hand.hand_state & hand_state.HandState.ACTIVE):
                continue

            if all(score > 21 for score in game.get_hand_scores(i)):
               continue

            if num_active_hands == 1: # only allow splitting once
                card_1_scores = blackjackcard.Power.from_card(game.player_hands[0].cards[0]).get_score()
                card_2_scores = blackjackcard.Power.from_card(game.player_hands[0].cards[1]).get_score()

                if card_1_scores == card_2_scores:
                    possible_moves[f"split_{i}"] = player_move.PlayerMove.ActionPair(InitialMove.PlayerActionInitial.SPLIT, 0)

        # hit and stand cases are dealt with by PlayerMove
            if not (hand.hand_state & hand_state.HandState.DOUBLING):
                possible_moves[f"double_{i}"] = player_move.PlayerMove.ActionPair(InitialMove.PlayerActionInitial.DOUBLE, i)
            # only one hand can be interacted with at a time
            break

        possible_moves.update(super(InitialMove, InitialMove).get_possible_moves(game))
        return possible_moves
