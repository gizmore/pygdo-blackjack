from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.blackjack.Game import Game
from gdo.core.GDT_UInt import GDT_UInt


class draw(Method):

    def gdo_trigger(self) -> str:
        return 'bj.draw'

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_UInt('amt').min(1).max(3).initial('1'),
        ]

    def gdo_execute(self) -> GDT:
        user = self._env_user
        game = Game.instance(user)
        amt = self.param_value('amt')
        if not game.running():
            return self.err('err_bj_not_running')
        cards = game.draw(amt)
        value = game.hand_value(game._hand)
        if value == 21:
            bj = game.has_blackjack()
            win = game.won(bj)
            if bj:
                return self.msg('msg_bj_draw_bj', [amt, game.render_hand(cards), win, game.get_credits()])
            else:
                return self.msg('msg_bj_draw_won', [amt, game.render_hand(cards), win, game.get_credits()])
        elif value > 21:
            win = game.lost()
            return self.err('msg_bj_busted', [amt, game.render_cards(cards), win, game.get_credits()])

        return self.msg('msg_bj_drawn', [amt, game.render_hand(cards)])
