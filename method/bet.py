from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.blackjack.module_blackjack import module_blackjack
from gdo.blackjack.Game import Game
from gdo.core.GDT_UInt import GDT_UInt
from gdo.payment_credits.GDT_Credits import GDT_Credits


class bet(Method):

    _game: Game

    def gdo_trigger(self):
        return 'bj.bet'

    def gdo_parameters(self):
        return [
            GDT_Credits('bet').not_null(),
        ]

    def gdo_execute(self) -> GDT:
        user = self._env_user
        mod = module_blackjack.instance()
        amt = self.param_value('bet')
        has = mod.get_credits(user)
        self._game = game = Game.instance(user)
        if game.has_bet():
            return self.err('err_bj_running')
        min_bet = mod.cfg_min_bet()
        if amt < min_bet:
            return self.err('err_bj_min_bet', [min_bet])
        if has < amt:
            return self.err('err_bj_credits', [has])

        cards = game.bet(amt)

        if game.has_blackjack():
            win = game.won(True)
            return self.msg('msg_bj_started_bj', [amt, game.render_cards(cards), win, game.get_credits()])

        self.msg('msg_bj_started', [amt, game.get_credits(), game.render_hand(cards)])
        return self.empty()

    def gdo_after_execute(self):
        self._game.save()
