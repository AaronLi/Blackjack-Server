import blackjackdeck
import blackjackcard
import collections

def test_create_deck():
    deck = blackjackdeck.BlackJackDeck(6)
    
    card_counts = collections.Counter(deck)

    for card, count in card_counts.items():
        assert 0<=card<=55
        assert count == deck.num_decks


def test_shuffle_deck():
    deck = blackjackdeck.BlackJackDeck(6)
    print("Unshuffled")
    for i in range(10):
        print(deck.draw_card())
    assert len(deck) == (len(blackjackdeck.BlackJackDeck.STANDARD_DECK) * deck.num_decks - 10)
    print("Shuffled")
    deck.shuffle_deck()
    for i in range(10):
        print(deck.draw_card())
    assert len(deck) == (len(blackjackdeck.BlackJackDeck.STANDARD_DECK) * deck.num_decks - 10)
