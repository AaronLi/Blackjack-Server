import random

from pymodm import MongoModel, fields, EmbeddedMongoModel

import blackjack


class Deck(EmbeddedMongoModel):
    cards = fields.ListField(fields.IntegerField(), default=list(blackjack.STANDARD_DECK * blackjack.NUM_DECKS), verbose_name="Cards")
    num_decks = fields.IntegerField(verbose_name="Number of Decks")
    shuffle_point = fields.IntegerField(verbose_name="Shuffle Point")

    def __fill_deck(self):
        """
        Fills the deck with a set of cards
        """
        self.cards.clear()
        for i in range(self.num_decks):
            self.cards.extend(blackjack.STANDARD_DECK)

    def shuffle_deck(self):
        """
        Refills the deck with cards and shuffles it. Sets a new shuffle point afterwards
        """
        self.__fill_deck()
        random.shuffle(self.cards)
        self.shuffle_point = random.randint(int(len(self.cards)*0.1), int(len(self.cards)*0.3))

    def draw_card(self):
        return self.cards.pop()

    def should_shuffle(self):
        return len(self.cards) < self.shuffle_point
