import random
from blackjack import blackjackcard


class BlackJackDeck(list):
    """
    A deck of cards, is actually a dict of how many of each card is in the deck (drawing a new card just picks a random key)
    """
    # If space becomes an issue, a dict of card counts could work

    def __init__(self, decks):
        super().__init__()
        self.num_decks = decks
        self.shuffle_point = 0

