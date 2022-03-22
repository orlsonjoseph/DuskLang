# ----------------------------------------------------------------------
# List.py
#
# List
# ----------------------------------------------------------------------

from core.nodes.__base__ import Statement

from core.resources.exceptions import NameError, TypeError
from core.resources.typing import Typing

class Indexing(Statement):
    def __init__(self, label, index) -> None:
        super().__init__()

        self.label, self.index = label, index
        self.computed_index = None

    def __str__(self) -> str:
        return f"Indexing [{self.label}, {self.index}]"

    def _eval(self, env):
        super()._eval(env)

        if self.label.name not in env:
            raise NameError(
                f"Name {self.label} has not been initialized. (Line {self.label.linepos}")
        
        _, d_type = env[self.label.name]

        if d_type.type in ['LIST']:
            self.computed_index = self.index._eval(env)

            if Typing.type_of(self.computed_index) == 'int':
                return env[self.label.name][0][self.computed_index]
           
            raise TypeError(
                f"List indices must be integers. (Line {self.index.linepos})")    

        raise TypeError(
            f"Indexing operation applies only to lists. (Line {self.label.linepos})")

    def _reassign(self, value, env):
        # Evaluation to catch potential errors
        self._eval(env)

        env[self.label.name][0][self.computed_index] = value
        return value # code executed successfully

class Reassign(Statement):
    def __init__(self, dest, value) -> None:
        super().__init__()

        self.dest, self.value = dest, value
    
    def __str__(self) -> str:
        return f"ListAssign [{self.dest}, {self.value}]"

    def _eval(self, env):
        super()._eval(env)
        
        fx = getattr(self.dest, '_reassign', None)

        if not callable(fx):
            raise TypeError(
                f"{self.dest} is not subscriptable. (Line {self.value.linepos})")

        value = self.value._eval(env)
        return self.dest._reassign(value, env)
        