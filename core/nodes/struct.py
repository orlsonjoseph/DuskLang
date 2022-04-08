# ----------------------------------------------------------------------
# struct.py
#
# Struct (statement)
# ----------------------------------------------------------------------

from core.nodes.__base__ import Statement
from core.nodes.typeid import TypeId

class Struct(Statement):
    def __init__(self, name, declarations, token) -> None:
        super().__init__()

        self.name, self.declarations = name, declarations
        self.token = token

    def __str__(self) -> str:
        return f"Struct <{self.name}>"

    def _eval(self, env, debug = True):        
        name = self.name._eval(env, eval = False)
        env[name] = [self.declarations, TypeId('struct')]
        return f"Struct {name}"
        