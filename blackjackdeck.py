import random
import blackjackcard

class BlackJackDeck(list):
    """
    A deck of cards, inherits all list functions and is designed to be used like a stack
     with higher addresses at the top of the stack
    """
    # If space becomes an issue, a dict of card counts could work
    STANDARD_DECK = [blackjackcard.Card(i) for i in range(52)]
    def __init__(self, decks):
        super().__init__()
        self.num_decks = decks
        self.shuffle_point = 0
    
    def __fill_deck(self):
        """
        Fills the deck with a set of cards
        """
        super().clear()
        for deck in range(self.num_decks):
            super().extend(list(BlackJackDeck.STANDARD_DECK))
    
    def shuffle_deck(self):
        """
        Refills the deck with cards and shuffles it. Sets a new shuffle point afterwards
        """
        self.__fill_deck()
        random.shuffle(self)
        self.shuffle_point = random.randint(int(len(self)*0.1), int(len(self)*0.3))

    def draw_card(self):
        return self.pop()

    def should_shuffle(self):
        return len(self) < self.shuffle_point