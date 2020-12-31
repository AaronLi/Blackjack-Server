import typing

import hand_state
import payoutfactor
from blackjackgamestate import gamestate, state


class Payout(gamestate.GameState):
    @staticmethod
    def enter(game: "BlackJackGame") -> "BlackJackGame":
        # TODO: pay balance to player
        payout = Payout.get_player_payout(game)
        print(f"You won {payout}₪")
        game.change_state(state.State.CONTINUE_PLAYING)
        return super(Payout, Payout).enter(game)

    @staticmethod
    def poll(game: "BlackJackGame") -> str:
        # TODO: require ack to continue to next state, allow poll for win reason and amount
        return super(Payout, Payout).poll(game)

    @staticmethod
    def input(game: "BlackJackGame", action_code: str) -> typing.Tuple["BlackJackGame", str]:
        return super(Payout, Payout).input(game, action_code)

    @staticmethod
    def exit(game: "BlackJackGame") -> "BlackJackGame":
        return super(Payout, Payout).exit(game)

    @staticmethod
    def get_valid_moves(game: "BlackJackGame") -> typing.Sequence[str]:
        return ["ack"]

    @staticmethod
    def get_player_payout(game: "BlackJackGame") -> int:
        """
        Calculate the player's payout.
        cases:
        player natural dealer natural
        player natural
        player loss
        player win
        :param game:
        :return:
        """
        payout = 0
        # getting a natural means you only have one hand, other cases need to take into account multiple hands
        if game.player_natural and game.dealer_natural:
            payout += payoutfactor.player_dealer_natural.get_payout(game.player_hands[0].bet)
            print("natural standoff")
        elif game.player_natural:
            # round down floats because we're the house xd
            print("natural!")
            payout += payoutfactor.player_natural.get_payout(game.player_hands[0].bet)
        else:
            dealer_hand_score = max((score for score in game.get_hand_scores(-1) if score <= 21), default=-1)
            dealer_bust = dealer_hand_score == -1
            for i, hand in enumerate(game.player_hands):
                player_hand_score = max((score for score in game.get_hand_scores(i) if score <= 21), default=-1)
                player_bust = player_hand_score == -1
                payout_model = None
                if hand.hand_state & hand_state.HandState.ACTIVE:
                    if player_bust:
                        # you lose your bet
                        print(f"hand {i} busted")
                        payout_model = payoutfactor.player_lose
                    elif player_hand_score > dealer_hand_score:
                        if hand.hand_state & hand_state.HandState.DOUBLING:
                            print(f"hand {i} doubled win!")
                            payout_model = payoutfactor.player_win_double
                        else:
                            print(f"hand {i} win!")
                            payout_model = payoutfactor.player_win
                    elif player_hand_score == dealer_hand_score:
                        print(f"hand {i} standoff")
                        payout_model = payoutfactor.stand_off
                    elif player_hand_score < dealer_hand_score:
                        print(f"hand {i} loss")
                        payout_model = payoutfactor.player_lose
                    elif dealer_bust:
                        # only player hands that didn't bust receive their money
                        if not player_bust:  # hand score is only -1 if the player busted (all player hand scores > 21)
                            if hand.hand_state & hand_state.HandState.DOUBLING:
                                print(f"hand {i}, double win! dealer bust")
                                payout_model = payoutfactor.player_win_double
                            else:
                                print(f"hand {i}, win! dealer bust")
                                payout_model = payoutfactor.player_win
                    print(payout_model, payout_model.get_payout(hand.bet))
                    payout += payout_model.get_payout(hand.bet)
        return payout
