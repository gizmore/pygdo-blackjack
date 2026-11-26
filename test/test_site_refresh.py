import unittest
from unittest.mock import MagicMock, patch

from gdo.base.Application import Application
from gdo.blackjack.method.site import site


class SiteRefreshTest(unittest.IsolatedAsyncioTestCase):
    async def test_play_rebuilds_status_form_after_command(self):
        with patch.object(Application, 'get_mode', return_value=None):
            page = site()
        old_form = page._form = MagicMock()
        new_form = MagicMock()
        action = MagicMock()
        action.env_copy.return_value = action
        action.args_copy.return_value = action
        action.execute.return_value = 'result'
        bar = MagicMock()
        bar.vertical.return_value = bar
        def rebuild():
            self.assertFalse(hasattr(page, '_form'))
            return new_form

        with patch.object(page, 'get_form', side_effect=rebuild) as get_form, \
             patch('gdo.blackjack.method.site.GDT_Bar', return_value=bar):
            await page.bj_method(lambda: action)
        self.assertFalse(hasattr(page, '_form'))
        get_form.assert_called_once_with()
        bar.add_fields.assert_called_once_with('result', new_form)
        self.assertIsNot(old_form, new_form)
