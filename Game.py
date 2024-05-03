from random import shuffle

from gdo.core.GDO_User import GDO_User


class Game:
    GAMES = {}

    _bet: int
    _user: GDO_User
    _cards: []
    _hand: []

    def __init__(self, user: GDO_User):
        self.bet = 0
        self.user = user
        self.cards = []
        self.hand = []
        self.shuffle()

    # def rply(self, key: str, args: List[Union[str, int]] = None) -> DOG_Message:
    #     return DOG_Message.LAST_MESSAGE.rply(key, args)

    def shuffle(self) -> None:
        self.user.send("msg_bj_shuffle")
        cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = cards * 8
        shuffle(self.cards)

    @classmethod
    def instance(cls, user: DOG_User) -> 'Game':
        uid = user.getID()
        if uid not in cls.GAMES:
            cls.GAMES[uid] = cls(user)
        return cls.GAMES[uid]

    def hasBet(self) -> bool:
        return self.bet > 0

    def bet(self, bet: int) -> List[Union[str, int]]:
        m = Module_DogBlackjack.instance()
        min_bet = m.cfgMinBet()
        have = m.getCredits(self.user)
        if bet < min_bet:
            self.rply('err_blackjack_min', [bet, have])
        elif have < bet:
            self.rply('err_blackjack_money', [bet, have])
        else:
            m.bet(self.user, bet)
            self.bet = bet
            self.hand = []
            return self.draw(2)
        return None

    def draw(self, amt: int = 1) -> List[str]:
        for _ in range(amt):
            self.hand.append(self.drawCard())
        return self.hand

    def drawCard(self) -> str:
        return self.cards.pop()

    def over(self, shuffle: bool = False) -> bool:
        self.bet = 0
        self.hand = []
        if shuffle or len(self.cards) < 32:
            self.shuffle()
        return True

    def handBusted(self, cards: List[str]) -> bool:
        return self.handValue(cards) > 21

    def handValue(self, cards: List[str], bj: Union[bool, None] = None) -> int:
        bj = False
        perms = []
        for card in cards:
            perms.append(self.cardValue(card))
        min_val = 137
        max_val = 0
        perms = Permutations(perms)
        for p in perms.generate():
            val_sum = sum(p)
            if val_sum == 21:
                bj = True
                return 21
            elif val_sum < 21:
                max_val = max(val_sum, max_val)
            min_val = min(val_sum, min_val)
        if len(cards) >= 5 and min_val <= 21:
            bj = True
            return 21
        if min_val > 21:
            return min_val
        return max_val

    def cardValue(self, card: str) -> List[int]:
        if card in ['10', 'J', 'Q', 'K']:
            return [10]
        elif card == 'A':
            return [11, 1]
        else:
            return [int(card)]

    def running(self) -> bool:
        if self.hasBet():
            return True
        self.rply('err_blackjack_no_game')
        return False

    def playerValue(self) -> int:
        return self.handValue(self.hand)

    def getCredits(self) -> int:
        return Module_DogBlackjack.instance().getCredits(self.user)

    def lost(self, bj: bool = False) -> int:
        m = Module_DogBlackjack.instance()
        m.saveGame(self.user, -self.bet, bj)
        loss = self.bet
        self.over()
        return loss

    def won(self, bj: bool = False) -> int:
        m = Module_DogBlackjack.instance()
        win = self.bet * (4 if bj else 2)
        m.saveGame(self.user, win, bj)
        self.over()
        return win

    def renderHand(self, cards: List[str]) -> str:
        return "bj_hand({}, {}, {})".format(len(cards), ', '.join(cards), self.handValue(cards))

    def getBet(self) -> int:
        return self.bet
