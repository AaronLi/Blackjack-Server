import enum
import typing, logging
import db.game
from blackjack import hand_state, payoutfactor
from blackjack.blackjackgamestate import gamestate, state, dispatcher


class GameResult(enum.Enum):
    WON = enum.auto()
    TIE = enum.auto()
    LOSS = enum.auto()


class Payout(gamestate.GameState):
    @staticmethod
    def enter(game: "db.game.Game") -> "db.game.Game":
        # TODO: pay balance to player
        payout = Payout.get_player_payout(game)[1]
        logging.info(f"Player {'x'} won {payout}₪")
        game.player.balance += payout
        game.player.save()
        return super(Payout, Payout).enter(game)

    @staticmethod
    def poll(game: "db.game.Game") -> str:
        result, winning = Payout.get_player_payout(game)
        return f"payout\n{result.name.lower()} {winning}\nmoves 1 {' '.join(Payout.get_valid_moves(game))}"

    @staticmethod
    def input(game: "db.game.Game", action_code: str) -> typing.Tuple["db.game.Game", str]:
        if action_code in Payout.get_valid_moves(game):
            game.change_state(state.State.CONTINUE_PLAYING)
        return game, dispatcher.Dispatcher.poll(game)

    @staticmethod
    def exit(game: "db.game.Game") -> "db.game.Game":
        return super(Payout, Payout).exit(game)

    @staticmethod
    def get_valid_moves(game: "db.game.Game") -> typing.Sequence[str]:
        return ["ack"]

    @staticmethod
    def get_player_payout(game: "db.game.Game") -> typing.Tuple[GameResult, int]:
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
            logging.info("natural standoff")
        elif game.player_natural:
            # round down floats because we're the house xd
            logging.info("natural!")
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
                        logging.info(f"hand {i} busted")
                        payout_model = payoutfactor.player_lose
                    elif player_hand_score > dealer_hand_score:
                        if hand.hand_state & hand_state.HandState.DOUBLING:
                            logging.info(f"hand {i} doubled win!")
                            payout_model = payoutfactor.player_win_double
                        else:
                            logging.info(f"hand {i} win!")
                            payout_model = payoutfactor.player_win
                    elif player_hand_score == dealer_hand_score:
                        logging.info(f"hand {i} standoff")
                        payout_model = payoutfactor.stand_off
                    elif player_hand_score < dealer_hand_score:
                        logging.info(f"hand {i} loss")
                        payout_model = payoutfactor.player_lose
                    elif dealer_bust:
                        # only player hands that didn't bust receive their money
                        if not player_bust:  # hand score is only -1 if the player busted (all player hand scores > 21)
                            if hand.hand_state & hand_state.HandState.DOUBLING:
                                logging.info(f"hand {i}, double win! dealer bust")
                                payout_model = payoutfactor.player_win_double
                            else:
                                logging.info(f"hand {i}, win! dealer bust")
                                payout_model = payoutfactor.player_win
                    logging.info(f"{payout_model} {payout_model.get_payout(hand.bet)}")
                    payout += payout_model.get_payout(hand.bet)
        wager_amount = sum(hand.bet for hand in game.player_hands)
        if payout < wager_amount:
            game_result = GameResult.LOSS
        elif payout == wager_amount:
            game_result = GameResult.TIE
        elif payout > wager_amount:
            game_result = GameResult.WON
        return game_result, payout
