import enum
from pymodm import fields

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