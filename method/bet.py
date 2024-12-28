from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.blackjack.module_blackjack import module_blackjack
from gdo.blackjack.Game import Game
from gdo.core.GDT_UInt import GDT_UInt


class bet(Method):
    def gdo_trigger(self):
        return 'bj.bet'

    def gdo_parameters(self):
        return [
            GDT_UInt('bet').not_null(),
        ]

    def gdo_execute(self) -> GDT:
        user = self._env_user
        mod = module_blackjack.instance()
        amt = self.param_value('bet')
        has = mod.get_credits(user)
        game = Game.instance(user)
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

        return self.reply('msg_bj_started', [amt, game.get_credits(), game.render_hand(cards)])
