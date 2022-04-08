# ----------------------------------------------------------------------
# let.py
#
# Let (statement)
# ----------------------------------------------------------------------

from threading import local
from core.nodes import struct
from core.nodes.__base__ import Statement
from core.nodes.typeid import TypeId

from core.resources.exceptions import NameError

class Let(Statement):
    def __init__(self, name, type, token) -> None:
        super().__init__()

        self.name, self.type = name, type
        self.token = token

    def __str__(self) -> str:
        return f"Let [{self.name}] {self.type}]"

    def _eval(self, env, **kwargs):
        label = self.name._eval(env, eval = False)

        if label in env:
            raise NameError(
                f"Name {label} already exists. (Line {self.token.linepos}")

        if self.type.is_primitive():
            env[label] = [None, self.type]
        else:
            # Structures
            struct = self.type._eval(env).capitalize()
            
            if struct not in env:
                raise NameError(
                    f"Name {label} not defined. (Line {self.token.linepos}")

            # Execute declaration statements
            struct, _ = env[struct]

            locals = {}
            env[label] = [locals, TypeId('locals')]

            for declaration in struct:
                declaration._eval(locals)

        return label