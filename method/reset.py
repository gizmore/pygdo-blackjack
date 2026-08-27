from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.base.WithRateLimit import WithRateLimit
from gdo.blackjack.module_blackjack import module_blackjack
from gdo.blackjack.Game import Game


class reset(Method):

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'bj.reset'

    @classmethod
    def gdo_trig(cls) -> str:
        return 'bjr'

    def gdo_method_hidden(self) -> bool:
        return True

    @WithRateLimit
    def gdo_execute(self) -> GDT:
        user = self._env_user
        mod = module_blackjack.instance()
        mod.reset(user)
        Game.reset(user)
        return self.msg('msg_bj_reset', (mod.get_credits(user),))
