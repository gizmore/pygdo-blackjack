import unittest
from unittest.mock import MagicMock, patch

from gdo.base.Application import Application
from gdo.blackjack.method.leave import leave
from gdo.core.ChallengeToken import verify


class LeaveTest(unittest.TestCase):
    def setUp(self):
        with patch.object(Application, 'get_mode', return_value=None):
            self.method = leave()
        self.method._env_user = MagicMock()
        self.method._env_user.get_name.return_value = 'player'
        self.method.msg = MagicMock(side_effect=lambda key, args: (key, args))
        self.method.err = MagicMock(side_effect=lambda key, *args: key)

    def test_millionaire_gets_signed_token(self):
        self.method._env_user.get_setting_value.return_value = 1_000_000
        module = MagicMock()
        module.file_path.return_value = '/unused'
        with patch('gdo.blackjack.method.leave.module_config_value', return_value=1_000_000), \
             patch('gdo.blackjack.method.leave.module_blackjack.instance', return_value=module), \
             patch('gdo.blackjack.method.leave.read_secret', return_value=b'k' * 32):
            key, (_, token) = self.method.gdo_execute()
        self.assertEqual('msg_bj_millionaire', key)
        self.assertTrue(verify(b'k' * 32, 'bj1', token))

    def test_below_million_cannot_receive_token_even_if_config_is_lower(self):
        self.method._env_user.get_setting_value.return_value = 999_999
        with patch('gdo.blackjack.method.leave.module_config_value', return_value=5), \
             patch('gdo.blackjack.method.leave.read_secret') as secret:
            self.assertEqual('err_bj_millionaire', self.method.gdo_execute())
            secret.assert_not_called()

    def test_missing_token_secret_fails_closed(self):
        self.method._env_user.get_setting_value.return_value = 1_000_000
        with patch('gdo.blackjack.method.leave.module_config_value', return_value=1_000_000), \
             patch('gdo.blackjack.method.leave.module_blackjack.instance', return_value=MagicMock()), \
             patch('gdo.blackjack.method.leave.read_secret', side_effect=FileNotFoundError):
            self.assertEqual('err_bj_token_unavailable', self.method.gdo_execute())

    def test_channel_token_is_sent_privately(self):
        self.method._env_user.get_setting_value.return_value = 1_000_000
        self.method._env_channel = MagicMock()
        self.method._env_http = False
        self.method._message = MagicMock()
        with patch('gdo.blackjack.method.leave.module_config_value', return_value=1_000_000), \
             patch('gdo.blackjack.method.leave.module_blackjack.instance', return_value=MagicMock()), \
             patch('gdo.blackjack.method.leave.read_secret', return_value=b'k' * 32):
            self.method.gdo_execute()
        self.method._message.reply_privately.assert_called_once_with()
