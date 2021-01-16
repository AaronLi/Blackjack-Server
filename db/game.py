import logging
from typing import List

from pymodm import MongoModel, fields

import blackjack
from blackjack import hand_state, blackjackcard
from blackjack.blackjackgamestate import dispatcher, state as game_state
from db.deck import Deck
from db.hand import Hand


class Game(MongoModel):
    player_hands = fields.EmbeddedDocumentListField(Hand, verbose_name="Player Hands",
                                                    default=[Hand(hand_state=hand_state.HandState.ACTIVE),
                                                             Hand()])

    player_natural = fields.BooleanField(default=False)
    dealer_natural = fields.BooleanField(default=False)

    dealer_hand = fields.EmbeddedDocumentField(Hand, verbose_name="Dealer Hand",
                                               default=Hand(hand_state=hand_state.HandState.ACTIVE))

    deck = fields.EmbeddedDocumentField(Deck, "deck", default=Deck(num_decks=blackjack.NUM_DECKS))

    state = fields.IntegerField(default=game_state.State.SETTING_BET)

    player = fields.ReferenceField("User", verbose_name="Player")
    last_move_time = fields.DateTimeField("Last Move")

    def setup_new_round(self):
        self.player_hands = [Hand([], hand_state.HandState.ACTIVE, self.player_hands[0].bet),
                             Hand([], hand_state.HandState.INACTIVE, 0)]
        self.player_natural = False
        self.dealer_natural = False
        self.dealer_hand = Hand([], hand_state.HandState.ACTIVE, 0)

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
            card_scores = blackjackcard.Power.from_card(card).get_score()
            if blackjackcard.Power.from_card(card) == blackjackcard.Power.ACE:
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

    def change_state(self, new_state: int):
        logging.debug(f"change from {game_state.State(self.state).name} to {game_state.State(new_state).name}")
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
        # TODO: replace str(str(card)) with str(int(card))
        response.append(
            f"dealer {len(self.dealer_hand.cards)} {' '.join(str(str(card)) if ((self.state >= game_state.State.DEALER_MOVE) or (i == 0)) else '-1' for i, card in enumerate(self.dealer_hand.cards))}")

        return '\n'.join(response)
