# ----------------------------------------------------------------------
# boolean.py
#
# Boolean
# ----------------------------------------------------------------------

from core.nodes.__base__ import Expression

class Boolean(Expression):
    def __init__(self, value) -> None:
        super().__init__()

        self.value = value

    def __str__(self) -> str:
        return f"Boolean <{self.value}>"

    def _eval(self, env, **kwargs):
        return bool(self.value)