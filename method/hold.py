from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.blackjack.Game import Game


class hold(Method):

    _game: Game

    @classmethod
    def gdo_trigger(cls) -> str:
        return "bj.hold"

    @classmethod
    def gdo_trig(cls) -> str:
        return 'bjh'

    def gdo_execute(self) -> GDT:
        user = self._env_user
        game = self._game = Game.instance(user)

        if not game.running():
            return self.err('err_bj_not_running')

        min_ = game.hand_value(game._hand)
        cards = game._dealer
        while game.hand_value(cards) < min_:
            cards.append(game.draw_card())

        if game.hand_value(cards) > 21:
            win = game.won(False)
            return self.msg('msg_bj_won', (game.render_cards(cards), win, game.get_credits()))

        if game.hand_value(cards) == min_:
            bet = game.on_draw()
            return self.err('msg_bj_lost_draw', (game.render_cards(cards), bet, game.get_credits()))

        loss = game.lost()
        return self.err('msg_bj_lost', (game.render_cards(cards), loss, game.get_credits()))

    def gdo_after_execute(self):
        self._game.save()
