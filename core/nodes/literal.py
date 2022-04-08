# ----------------------------------------------------------------------
# literal.py
#
# Literal
# ----------------------------------------------------------------------

from core.nodes.__base__ import Expression

from core.resources.exceptions import NameError

class Literal(Expression):
    def __init__(self, name, token) -> None:
        super().__init__()
        
        self.name, self.token = name, token

    def __str__(self) -> str:
        return f"Literal '{self.name}'"

    def _eval(self, env, **kwargs):        
        if "eval" in kwargs and not kwargs["eval"]: return self.name
        
        # Evaluating a literal always seeks out the value
        if env is None:
            raise Exception("oof")

        if self.name not in env:
            raise NameError(f"Name '{self.name}' not defined. (Line {self.token.linepos})")
        
        value, _ = env[self.name]
        
        if isinstance(value, Expression):
            return value._eval(env)

        return value