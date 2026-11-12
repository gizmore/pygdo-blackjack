from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.base.Util import module_config_value
from gdo.core.ChallengeToken import bj_secret_path, issue, read_secret

class leave(Method):

        @classmethod
        def gdo_trigger(cls) -> str:
            return 'bj.leave'

        @classmethod
        def gdo_trig(cls) -> str:
            return 'bjl'

        def gdo_method_hidden(self) -> bool:
            return True

        def gdo_execute(self) -> GDT:
            score_have = self._env_user.get_setting_value('bj_credits')
            score_required = max(1_000_000, module_config_value('blackjack', 'bj_millionaire'))
            if score_have < score_required:
                return self.err('err_bj_millionaire', (score_required, score_have, score_required - score_have))
            try:
                secret = read_secret(bj_secret_path())
                solution = issue(secret, 'bj1', self._env_user.get_name())
            except (OSError, ValueError):
                return self.err('err_bj_token_unavailable')
            if self._env_channel is not None and not self._env_http:
                message = getattr(self, '_message', None)
                if message is None:
                    return self.err('err_bj_token_private')
                message.reply_privately()
            return self.msg('msg_bj_millionaire', (score_required, solution))
