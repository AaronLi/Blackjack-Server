import enum


class State(enum.IntEnum):
    SETTING_BET = 0 # choose how much you're betting
    SHUFFLING_DECK = 1 # shuffle the deck and insert shuffle card, this requires no player interaction
    INITIAL_MOVE = 2 # deal the first two cards to the player and dealer
    PLAYER_MOVE = 3 # play your hands
    DEALER_MOVE = 4 # Dealer draws cards
    PAYOUT = 5 # exchange money
    CONTINUE_PLAYING = 6 # play again or end game
    END = 7