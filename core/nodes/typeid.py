# ----------------------------------------------------------------------
# typeid.py
#
# Type Identifier
# ----------------------------------------------------------------------

from core.nodes.__base__ import Expression
from core.resources.constants import BUILTIN_TYPES, PRIMITIVES

class TypeId(Expression):
    def __init__(self, type) -> None:
        super().__init__()

        self.type = type.upper()

    def __str__(self) -> str:
        return f"Type <{self.type}>"

    def _eval(self, env, **kwargs):
        return self.type

    def is_primitive(self):
        return self.type in BUILTIN_TYPES
