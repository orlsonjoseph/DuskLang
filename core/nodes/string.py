# ----------------------------------------------------------------------
# string.py
#
# String
# ----------------------------------------------------------------------

from core.nodes.__base__ import Expression

class String(Expression):
    def __init__(self, value) -> None:
        super().__init__()

        self.value = value.strip('\"')

    def __str__(self) -> str:
        return f"String <{self.value}>"

    def _eval(self, env):
        super()._eval(env)

        return str(self.value)
