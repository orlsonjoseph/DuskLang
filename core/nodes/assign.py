# ----------------------------------------------------------------------
# assign.py
#
# Assign
# ----------------------------------------------------------------------

from core.nodes.__base__ import Statement

from core.resources.exceptions import NameError, TypeError
from core.resources.typing import Typing

class Assign(Statement):
    def __init__(self, label, value) -> None:
        super().__init__()

        self.label, self.value = label, value
    
    def __str__(self) -> str:
        return f"Assign [{self.label}] {self.value}"

    def _eval(self, env):
        super()._eval(env)

        if self.label.name not in env:
            raise NameError(
                f"Name {self.label} has not been initialized. (Line {self.label.linepos}")

        _, d_type = env[self.label.name]

        if d_type.type in ['LIST']:
            value = [v._eval(env) for v in self.value]
            
        else:
            value = self.value._eval(env)
             
            if not Typing.compare(env[self.label.name], value):
                raise TypeError(
                    "Unable to assign type TODO to {self.label.name}. (Line {self.operator.linepos})")

        # Only value is updated - type remains intact
        env[self.label.name] = [value, d_type]

        return (self.label.name, value, d_type._eval(env))