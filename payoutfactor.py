from dataclasses import dataclass

@dataclass
class PayoutFactor:
    bet_return_factor: float
    return_bet: bool

    def get_payout(self, bet):
        total = self.bet_return_factor * bet
        if self.return_bet:
            total += bet

        return total

player_natural = PayoutFactor(1.5, True)
player_dealer_natural = PayoutFactor(0, True)
dealer_natural = PayoutFactor(0, False)

player_win = PayoutFactor(1, True)
player_win_double = PayoutFactor(2, True)
player_lose = PayoutFactor(0, False)
stand_off = PayoutFactor(0, True)

if __name__ == '__main__':
    print(player_win.get_payout(10))