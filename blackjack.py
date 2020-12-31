from typing import List

from dataclasses import dataclass
import blackjackcard
import blackjackdeck
import hand_state
from blackjackgamestate import state, dispatcher


@dataclass
class BlackJackHand:
    cards: list
    hand_state: hand_state.HandState
    bet: int


class BlackJackGame:
    MAX_BET = 500
    BET_SIZES = [5, 10, 25, 50, 100]

    def __init__(self) -> None:
        super().__init__()
        self.player_hands = [BlackJackHand([], hand_state.HandState.ACTIVE, 0),
                             BlackJackHand([], hand_state.HandState.INACTIVE, 0)]
        self.player_natural = False
        self.dealer_natural = False
        self.dealer_hand = BlackJackHand([], hand_state.HandState.ACTIVE, 0)
        self.deck = blackjackdeck.BlackJackDeck(6)
        self.state = state.State.SETTING_BET

    def setup_new_round(self):
        self.player_hands = [BlackJackHand([], hand_state.HandState.ACTIVE, self.player_hands[0].bet),
                             BlackJackHand([], hand_state.HandState.INACTIVE, 0)]
        self.player_natural = False
        self.dealer_natural = False
        self.dealer_hand = BlackJackHand([], hand_state.HandState.ACTIVE, 0)

    def get_hand_scores(self, hand_number) -> List[int]:
        """
        Get the score of a given hand of cards, -1 gets the scores of the dealer's hand
        :param hand_number:
        :return:
        """
        scores = [0]
        cards_to_score = []
        if hand_number >= len(self.player_hands):
            return []
        elif 0 <= hand_number <= len(self.player_hands):
            cards_to_score = self.player_hands[hand_number].cards
        elif hand_number == -1:
            cards_to_score = self.dealer_hand.cards

        for card in cards_to_score:
            card_scores = card.get_power().get_score()
            if card.get_power() == blackjackcard.Power.ACE:
                if len(scores) == 1:
                    scores = [scores[0] + card_scores[0], scores[0] + card_scores[1]]
                elif len(scores) == 2:
                    scores[0] += card_scores[0]
                    scores[1] += card_scores[0]
            else:
                if len(scores) == 1:
                    scores[0] += card_scores[0]
                elif len(scores) == 2:
                    scores[0] += card_scores[0]
                    scores[1] += card_scores[0]
        return scores

    def change_state(self, new_state: state.State):
        dispatcher.Dispatcher.exit(self)
        self.state = new_state
        dispatcher.Dispatcher.enter(self)

    def __str__(self):
        response = []

        # string for section, number of hands, list of hands
        hand_string = []
        hand_string.append(f"hands {len(self.player_hands)}")

        for hand in self.player_hands:
            # each hand has a state integer, hand bet, number of cards, list of cards
            hand_string.append(f"{hand.hand_state} {hand.bet} {len(hand.cards)} {' '.join(str(c) for c in hand.cards)}")

        response.append(' '.join(hand_string))

        # only show the first card of the dealer
        # number of cards the dealer has, first card
        response.append(f"dealer {len(self.dealer_hand.cards)} {self.dealer_hand.cards[0]}")

        return '\n'.join(response)
