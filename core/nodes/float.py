# ----------------------------------------------------------------------
# float.py
#
# Float
# ----------------------------------------------------------------------

from core.nodes.__base__ import Expression

class Float(Expression):
    def __init__(self, value) -> None:
        super().__init__()

        self.value = value

    def __str__(self) -> str:
        return f"Float <{self.value}>"

    def _eval(self, env, **kwargs):
        return float(self.value)