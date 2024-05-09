from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDT_User import GDT_User


class stats(Method):

    def gdo_trigger(self) -> str:
        return 'bj.stats'

    def gdo_parameters(self) -> [GDT]:
        return [
            GDT_User('user'),
        ]

    def gdo_execute(self):
        user = self.param_value('user')
        if not user:
            return self.show_global_stats()
        else:
            return self.show_user_stats(user)

    def show_global_stats(self):
        pass

    def show_user_stats(self, user):
        pass

        