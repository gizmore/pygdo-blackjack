import unittest
from unittest.mock import MagicMock, patch

from gdo.base.Application import Application
from gdo.blackjack.method.table import table


class TableTest(unittest.TestCase):
    def setUp(self):
        with patch.object(Application, 'get_mode', return_value=None):
            self.method = table()
        self.method._env_user = MagicMock()
        self.method.reply = MagicMock(side_effect=lambda key, args=None: (key, args))

    def test_active_game_shows_both_hands_without_mutating(self):
        game = MagicMock()
        game.running.return_value = True
        game._hand = ['♠2', '♥10']
        game._dealer = ['♠5']
        game.render_hand.return_value = 'player cards'
        game.render_cards.return_value = 'dealer cards'
        with patch('gdo.blackjack.method.table.Game.instance', return_value=game):
            self.assertEqual(('msg_bj_table', ('player cards', 'dealer cards')), self.method.gdo_execute())
        game.render_hand.assert_called_once_with(['♠2', '♥10'])
        game.render_cards.assert_called_once_with(['♠5'])
        game.save.assert_not_called()

    def test_no_running_game(self):
        game = MagicMock()
        game.running.return_value = False
        with patch('gdo.blackjack.method.table.Game.instance', return_value=game):
            self.assertEqual(('err_bj_not_running', None), self.method.gdo_execute())
        game.render_hand.assert_not_called()
