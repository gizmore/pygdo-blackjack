from random import shuffle

from gdo.base.Cache import Cache
from gdo.base.Trans import t
from gdo.base.Util import Permutations, msg
from gdo.blackjack.module_blackjack import module_blackjack
from gdo.core.GDO_User import GDO_User


class Game():
    _user: GDO_User
    _bet: int
    _cards: []
    _hand: []

    @classmethod
    def instance(cls, user: 'GDO_User') -> 'Game':
        if game := Cache.get('bj_game', user.get_id()):
            return game
        game = Game(user)
        Cache.set('bj_game', user.get_id(), game)
        return game

    @classmethod
    def reset(cls, user: 'GDO_User'):
        Cache.remove('bj', user.get_id())

    def __init__(self, user: 'GDO_User'):
        self._bet = 0
        self._user = user
        self._cards = []
        self._hand = []
        self.shuffle()

    def shuffle(self) -> None:
        msg('msg_bj_shuffle')
        cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self._cards = cards * 8
        shuffle(self._cards)

    def has_bet(self) -> bool:
        return self._bet > 0

    def bet(self, bet: int):
        m = module_blackjack.instance()
        m.bet(self._user, bet)
        self._bet = bet
        return self.draw(2)

    def draw(self, amt: int = 1) -> list[str]:
        for _ in range(amt):
            self._hand.append(self.draw_card())
        return self._hand

    def draw_card(self) -> str:
        return self._cards.pop()

    def has_blackjack(self) -> bool:
        if len(self._hand) == 5:
            return True
        if len(self._hand) == 2 and self.hand_value(self._hand) == 21:
            return True
        return False

    def over(self, shuffle_: bool = False) -> bool:
        self._bet = 0
        self._hand = []
        if shuffle_ or len(self._cards) < 32:
            self.shuffle()
        return True

    def hand_busted(self, cards: list[str]) -> bool:
        return self.hand_value(cards) > 21

    def hand_value(self, cards: list[str]) -> int:
        perms = []
        for card in cards:
            perms.append(self.card_values(card))
        min_val = 1337
        max_val = 0
        perms = Permutations(perms)
        for p in perms.generate():
            val_sum = sum(p)
            if val_sum == 21:
                return 21
            elif val_sum < 21:
                max_val = max(val_sum, max_val)
            min_val = min(val_sum, min_val)
        if len(cards) >= 5 and min_val <= 21:
            return 21
        if min_val > 21:
            return min_val
        return max_val

    def card_values(self, card: str) -> list[int]:
        if card in ['10', 'J', 'Q', 'K']:
            return [10]
        elif card == 'A':
            return [11, 1]
        else:
            return [int(card)]

    def running(self) -> bool:
        return self.has_bet()

    def player_value(self) -> int:
        return self.hand_value(self._hand)

    def get_credits(self) -> int:
        return module_blackjack.instance().get_credits(self._user)

    def lost(self) -> int:
        m = module_blackjack.instance()
        m.save_game(self._user, -self._bet, False)
        loss = self._bet
        self.over()
        return loss

    def won(self, bj: bool) -> int:
        m = module_blackjack.instance()
        win = self._bet * (4 if bj else 2)
        m.save_game(self._user, win, bj)
        self.over()
        return win

    def render_hand(self, cards: list[str]) -> str:
        if len(cards):
            return t('bj_hand', [len(cards), self.render_cards(cards)])
        return t('bj_no_cards')

    def render_cards(self, cards: list[str]) -> str:
        return ', '.join(cards) + f" ({self.hand_value(cards)} {t('bj_points')})"

    def get_bet(self) -> int:
        return self._bet

