from gdo.core.GDT_UInt import GDT_UInt


class GDT_BlackjackCredits(GDT_UInt):
    """Play money, independent of payment credits."""

    def __init__(self, name: str):
        super().__init__(name)
        self.label('bj_credits').icon('money')
