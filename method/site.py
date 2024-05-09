from gdo.blackjack.Game import Game
from gdo.blackjack.method.draw import draw
from gdo.blackjack.method.hold import hold
from gdo.blackjack.method.reset import reset
from gdo.blackjack.module_blackjack import module_blackjack
from gdo.blackjack.method.bet import bet
from gdo.core.GDT_UInt import GDT_UInt
from gdo.form.GDT_Form import GDT_Form
from gdo.form.GDT_Submit import GDT_Submit
from gdo.form.MethodForm import MethodForm
from gdo.ui.GDT_Bar import GDT_Bar


class site(MethodForm):

    def gdo_trigger(self) -> str:
        return ''

    def gdo_create_form(self, form: GDT_Form) -> None:
        mod = module_blackjack.instance()
        user = self._env_user
        game = Game.instance(user)
        num_played = user.get_setting_value('bj_played')
        num_won = user.get_setting_value('bj_won')
        won_percent = num_won / num_played * 100 if num_played > 0 else 50
        balance = user.get_setting_value('bj_credits')
        form.text('info_blackjack', [num_played, num_won, won_percent, balance, game.render_hand(game._hand)])
        form.add_field(GDT_UInt('bet').label('btn_bet').not_null().initial('10'))
        form.actions().add_field(
            GDT_Submit('new_bet').text('btn_bet').calling(self.bet),
            GDT_Submit('draw').text('btn_draw_card').calling(self.draw),
            GDT_Submit('hold').text('btn_hold_cards').calling(self.hold),
            GDT_Submit('reset').text('btn_reset').calling(self.reset),
        )
        # super().gdo_create_form(form)

    def bet(self):
        return self.bj_method(bet)

    def draw(self):
        return self.bj_method(draw)

    def hold(self):
        return self.bj_method(hold)

    def reset(self):
        return self.bj_method(reset)

    def bj_method(self, method_class):
        method = method_class()
        gdt = method.env_copy(self).args_copy(self).execute()
        return GDT_Bar().vertical().add_field(gdt, self.get_form(True))
