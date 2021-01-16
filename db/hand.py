from pymodm import MongoModel, fields, EmbeddedMongoModel

from blackjack import hand_state


class Hand(EmbeddedMongoModel):
    cards = fields.ListField(fields.IntegerField("Card"), verbose_name="Cards", default=[], blank=True)
    hand_state = fields.IntegerField("Hand Flags", default=hand_state.HandState.INACTIVE)
    bet = fields.IntegerField("Bet", default=0)
