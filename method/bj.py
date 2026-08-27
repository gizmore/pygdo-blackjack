from gdo.base.GDT import GDT
from gdo.base.Method import Method


class bj(Method):

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'blackjack'

    @classmethod
    def gdo_trig(cls) -> str:
        return 'bj'

    def gdo_execute(self) -> GDT:
        return self.reply('msg_bj_commands')
