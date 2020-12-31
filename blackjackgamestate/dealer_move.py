from typing import Sequence

import typing

from blackjackgamestate import gamestate, dispatcher, state


class DealerMove(gamestate.GameState):
    """
    The dealer's turn to draw cards
    Stops at score >= 17
    If the dealer got a natural in their initial move (InitialMove state), we won't go to DealerMove
    we will go straight to payout
    """

    @staticmethod
    def enter(game: "BlackJackGame") -> "BlackJackGame":
        return super(DealerMove, DealerMove).enter(game)

    @staticmethod
    def poll(game: "BlackJackGame") -> str:
        valid_moves = DealerMove.get_valid_moves(game)

        valid_moves_string = f"moves {len(valid_moves)} {' '.join(valid_moves)}"

        return '\n'.join(("dealermove", str(game), valid_moves_string))

    @staticmethod
    def input(game: "BlackJackGame", action_code: str) -> typing.Tuple["BlackJackGame", str]:
        if action_code in DealerMove.get_valid_moves(game):
            if action_code == "ack":
                # maybe only do this when receiving ack?
                if any(17 <= score <= 21 for score in game.get_hand_scores(-1)):
                    # dealer stops normally
                    game.change_state(state.State.PAYOUT)
                elif all(score > 21 for score in game.get_hand_scores(-1)):
                    # dealer busted
                    game.change_state(state.State.PAYOUT)
                else:
                    game.dealer_hand.cards.append(game.deck.draw_card())

        return game, dispatcher.Dispatcher.poll(game)

    @staticmethod
    def exit(game: "BlackJackGame") -> "BlackJackGame":
        return super(DealerMove, DealerMove).exit(game)

    @staticmethod
    def get_valid_moves(game: "BlackJackGame") -> typing.Sequence[str]:
        return 'ack',
