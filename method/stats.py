from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDT_User import GDT_User


class stats(Method):

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'bj.stats'

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_User('user'),
        ]

    def gdo_execute(self) -> GDT:
        user = self.param_value('user')
        if not user:
            return self.show_global_stats()
        else:
            return self.show_user_stats(user)

    def show_global_stats(self) -> GDT:
        pass

    def show_user_stats(self, user) -> GDT:
        pass

        