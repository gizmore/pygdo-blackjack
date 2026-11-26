from gdo.base.Method import Method
from gdo.blackjack.Game import Game


class table(Method):
    @classmethod
    def gdo_trigger(cls):
        return 'bj.table'

    def gdo_method_hidden(self):
        return True

    def gdo_execute(self):
        game = Game.instance(self._env_user)
        if not game.running():
            return self.reply('err_bj_not_running')
        return self.reply('msg_bj_table', (game.render_hand(game._hand),
                                           game.render_cards(game._dealer)))
