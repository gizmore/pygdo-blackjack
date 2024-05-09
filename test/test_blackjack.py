import os
import unittest

from gdo.base.Application import Application
from gdo.base.ModuleLoader import ModuleLoader
from gdo.base.Util import Random
from gdotest.TestUtil import web_plug, reinstall_module, cli_plug


class BlackJackTest(unittest.TestCase):

    def setUp(self):
        Application.init(os.path.dirname(__file__ + "/../../../../"))
        loader = ModuleLoader.instance()
        loader.load_modules_db(True)
        loader.init_modules()
        reinstall_module('blackjack')
        loader.init_cli()
        return self

    def test_01_game_reset(self):
        out = cli_plug(None, 'bj.reset')
        self.assertIn('Balance:', out, 'Blackjack does not reset.')

    def test_02_game_min_bet(self):
        out = cli_plug(None, 'bj.bet 5')
        self.assertIn('You have to bet at least', out, 'Blackjack does not capture min bet.')

    def test_03_game_start(self):
        cli_plug(None, 'bj.reset')
        Random.init(8)
        out = cli_plug(None, 'bj.bet 25')
        self.assertIn('have 75', out, 'Cannot bet half money #1.')
        self.assertIn('bet 25', out, 'Cannot bet half money #2.')
        self.assertIn('You hold 2 cards:', out, 'Cannot bet half money #2.')

    def test_04_game_lose_with_3_cards(self):
        Random.init(22)
        cli_plug(None, 'bj.reset')
        out = cli_plug(None, 'bj.bet 50')
        self.assertIn('have 50', out, 'Cannot bet half my money #3.')
        out = cli_plug(None, 'bj.draw')
        self.assertIn('1 card', out, 'Cannot bet half my money #4.')
        out = cli_plug(None, 'bj.hold')
        self.assertIn('You lost your 50 and now have 50.', out, 'Cannot bet half my money #5.')

    def test_05_busted(self):
        Random.init(23)
        cli_plug(None, 'bj.reset')
        out = cli_plug(None, 'bj.bet 25')
        self.assertIn('have 75', out, 'Cannot get busted #1')
        out = cli_plug(None, 'bj.draw')
        self.assertIn('You draw 1 card', out,'Cannot get busted #2')
        self.assertIn('Busted!', out, 'Cannot get busted #3')
        self.assertIn('have 75.', out, 'Cannot get busted #4')

    def test_06_site(self):
        out = web_plug('blackjack.site.html').post({'btn_reset': '1', 'bet': '23'}).exec()
        self.assertIn('value="23"', out, 'BJ Form does not fill old bet.')


if __name__ == '__main__':
    unittest.main()
