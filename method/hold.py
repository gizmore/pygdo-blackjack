from gdo.base.Method import Method
from gdo.blackjack.Game import Game


class hold(Method):

    def gdo_trigger(self) -> str:
        return "bj.hold"

    def gdo_execute(self):
        user = self._env_user
        game = Game.instance(user)

        if not game.running():
            return self.reply('err_bj_not_running')

        min_ = game.hand_value(game._hand)
        cards = [game.draw_card(), game.draw_card()]
        while game.hand_value(cards) <= min_:
            cards.append(game.draw_card())

        if game.hand_value(cards) > 21:
            win = game.won(False)
            return self.reply('msg_bj_won', [game.render_cards(cards), win, game.get_credits()])

        loss = game.lost()
        return self.reply('msg_bj_lost', [game.render_cards(cards), loss, game.get_credits()])
