# ----------------------------------------------------------------------
# typeid.py
#
# Type Identifier
# ----------------------------------------------------------------------

from core.nodes.__base__ import Expression

class TypeId(Expression):
    def __init__(self, type) -> None:
        super().__init__()

        self.type = type

    def __str__(self) -> str:
        return f"Type <{self.type.upper()}>"

    def _eval(self, env):
        super()._eval(env)

        return self.type
