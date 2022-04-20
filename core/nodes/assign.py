# ----------------------------------------------------------------------
# assign.py
#
# Assign
# ----------------------------------------------------------------------

from core.nodes.__base__ import Statement

from core.resources.exceptions import TypeError
from core.resources.typing import Typing

class Assign(Statement):
    def __init__(self, destination, expression, token) -> None:
        super().__init__()

        self.destination, self.expression = destination, expression
        self.token = token
        
    def __str__(self) -> str:
        return f"Assign [{self.destination}] {self.expression}"

    def _eval(self, env, **kwargs):
        # If assign on Indexing; then override function
        # INFO Workaround python passing by object call rather than ref
        if type(self.destination).__name__ == 'Indexing':
            return self.destination._eval(env, eval=True, target=self.expression)

        name = self.destination._eval(env, eval=False)
            
        _, d_type = env[name]
        
        # If assign on Prefix / Struct; then override function
        if d_type.type in ['LOCALS']:
            return self.destination._assign(env, target=self.expression)

        value = self.expression._eval(env)

        if not d_type.type in ['GRAPH', 'LIST', 'STRUCT']:
            if not Typing.compare(env[name], value):
                raise TypeError(
                    "Unable to assign type TODO to {name}. (Line {self.token.linepos})")

        # Only value is updated - type remains intact
        env[name] = [value, d_type]
        return [name, value, d_type._eval(env)]