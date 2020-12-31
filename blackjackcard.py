import enum

class Suit(enum.IntEnum):
    HEARTS = 0
    DIAMONDS = 1
    SPADES = 2
    CLUBS = 3

    @staticmethod
    def from_card(card):
        return Suit(card//13)

class Power(enum.IntEnum):
    ACE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    TEN = 9
    JACK = 10
    QUEEN = 11
    KING = 12

    @staticmethod
    def from_card(card):
        return Power(card%13)

    def get_score(self):
        if self == Power.ACE:
            return [1, 11]
        elif Power.TWO <= self <= Power.TEN:
            return [self+1]
        elif self >= Power.TEN:
            return [10]
class Card(int):
    def get_suit(self) -> Suit:
        return Suit.from_card(self)
    
    def get_power(self) -> Power:
        return Power.from_card(self)
    
    def __str__(self):
        return f"{self.get_power().name} of {self.get_suit().name}"