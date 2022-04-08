# ----------------------------------------------------------------------
# undefined.py
#
# Undefined
# ----------------------------------------------------------------------

from core.nodes.__base__ import Expression
from core.resources.constants import EMPTY_STRING

class Undefined(Expression):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return EMPTY_STRING

    def _eval(self, env, **kwargs):
        return None