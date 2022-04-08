# ----------------------------------------------------------------------
# number.py
#
# Number
# ----------------------------------------------------------------------

from core.nodes.__base__ import Expression

class Number(Expression):
    def __init__(self, value) -> None:
        super().__init__()

        self.value = value

    def __str__(self) -> str:
        return f"Number <{self.value}>"

    def _eval(self, env, **kwargs):
        return int(self.value)