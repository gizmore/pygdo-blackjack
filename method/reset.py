from gdo.base.Method import Method
from gdo.blackjack.module_blackjack import module_blackjack
from gdo.blackjack.Game import Game


class reset(Method):

    def gdo_trigger(self) -> str:
        return 'bj.reset'

    def gdo_execute(self):
        user = self._env_user
        mod = module_blackjack.instance()
        Game.reset(user)
        mod.reset(user)
        return self.reply('msg_bj_reset', [mod.get_credits(user)])
