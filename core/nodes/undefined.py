# ----------------------------------------------------------------------
# undefined.py
#
# Undefined
# ----------------------------------------------------------------------

from core.nodes.__base__ import Expression
from core.resources.constants import EMPTY_STRING

class Undefined(Expression):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return EMPTY_STRING

    def _eval(self, env, **kwargs):
        super()._eval(env)

        return None