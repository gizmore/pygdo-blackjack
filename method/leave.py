from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.base.Util import module_config_value, Files, get_module
import hashlib

class leave(Method):

        @classmethod
        def gdo_trigger(cls) -> str:
            return 'bj.leave'

        def gdo_execute(self) -> GDT:
            score_have = self._env_user.get_setting_value('bj_credits')
            score_required = module_config_value('blackjack', 'bj_millionaire')
            if score_have < score_required:
                return self.err('err_bj_millionaire', (score_required, score_have, score_required - score_have))
            solution = self.get_solution_blackjack(self._env_user.render_name(), Files.get_contents(get_module('blackjack').file_path('secret.txt')))
            return self.msg('msg_bj_millionaire', (score_required, solution))

        def md5_hex(self, s: str) -> str:
            return hashlib.md5(s.encode("utf-8")).hexdigest()

        def get_solution_blackjack(self, playername: str, dog_password: str) -> str:
            pname = playername.lower()
            h = self.md5_hex(dog_password + self.md5_hex(pname) + dog_password)[1:17]
            return f"{pname}!{h}!rich"
        