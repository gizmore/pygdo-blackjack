from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDT import GDT
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_UInt import GDT_UInt
from gdo.ui.GDT_Link import GDT_Link


class module_blackjack(GDO_Module):

    ##########
    # Config #
    ##########

    def gdo_module_config(self) -> list[GDT]:
        return [
            GDT_UInt('bj_min_bet').initial('10').min(1).max(1000000),
            GDT_UInt('bj_games').initial('0').writable(False),
            GDT_UInt('bj_games_won').initial('0').writable(False),
            GDT_UInt('bj_games_lost').initial('0').writable(False),
            GDT_UInt('bj_money_won').initial('0').writable(False),
            GDT_UInt('bj_money_lost').initial('0').writable(False),
        ]

    def cfg_min_bet(self) -> int:
        return self.get_config_value('bj_min_bet')

    def gdo_init_sidebar(self, page):
        page._left_bar.add_field(GDT_Link().href(self.href('site')).text('module_blackjack'))

    ###############
    # User Config #
    ###############

    def gdo_user_config(self) -> list[GDT]:
        return [
            GDT_UInt('bj_credits').initial('100'),
            GDT_UInt('bj_played').initial('0'),
            GDT_UInt('bj_won').initial('0'),
            GDT_UInt('bj_lost').initial('0'),
        ]

    def get_credits(self, user: GDO_User) -> int:
        return user.get_setting_value('bj_credits')

    def reset(self, user: GDO_User):
        user.reset_setting('bj_credits')

    ########
    # Game #
    ########
    def bet(self, user: GDO_User, bet: int):
        user.increase_setting('bj_credits', -bet)
        self.increase_config_val('bj_money_won', bet)

    def save_game(self, user: GDO_User, amt: int, bj: bool):
        self.increase_config_val('bj_games', 1)
        if amt > 0:
            user.increase_setting('bj_credits', amt)
        user.increase_setting('bj_played', 1)
        self.increase_config_val('bj_games', 1)
        if amt > 0:
            self.increase_config_val('bj_games_lost', 1)
            self.increase_config_val('bj_money_lost', amt)
            user.increase_setting('bj_won', 1)
        else:
            self.increase_config_val('bj_games_won', 1)
            self.increase_config_val('bj_money_won', -amt)
            user.increase_setting('bj_lost', 1)



