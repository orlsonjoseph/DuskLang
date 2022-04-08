# ----------------------------------------------------------------------
# Prefix.py
#
# Prefix
# ----------------------------------------------------------------------

from core.nodes.__base__ import Expression

from core.resources.exceptions import AttributeError, NameError, TypeError
from core.resources.typing import Typing

class Prefix(Expression):
    def __init__(self, prefix, endpoint, token) -> None:
        super().__init__()
        
        self.prefix, self.endpoint = prefix, endpoint
        self.token = token

    def __str__(self) -> str:
        return f"[Prefix {self.prefix} {self.endpoint}]"

    def _eval(self, env, **kwargs):
        if "eval" in kwargs and not kwargs["eval"]:
            # Not able to go further due to reference limitations
            return self.prefix._eval(env, eval=False)

        locals = self.prefix._eval(env, eval=True)
        
        # Indexing of struct attribute
        if type(self.endpoint).__name__ == 'Indexing':
            return self.endpoint._eval(locals, eval=False)

        label = self.endpoint._eval(locals, eval=False)
        
        if locals is None:
            raise AttributeError(
                f"Unknown attribute {label}. (Line {self.token.linepos})")
    
        if label not in locals:
            raise NameError(
                f"Attribute '{label}' not defined. (Line {self.token.linepos})")

        return self.endpoint._eval(locals, eval=True)

    def _assign(self, env, **kwargs):
        if "target" not in kwargs:
            raise KeyError(
                f"Structure assignment target unspecified. (Line {self.token.linepos})")
                
        target = kwargs["target"]._eval(env, eval=True)

        # Verify that prefixes exist
        self._eval(env, eval=True)
        
        # No error; move forward
        locals = self.prefix._eval(env, eval=True)

        if type(self.endpoint).__name__ == 'Indexing':
            return self.endpoint._eval(locals, eval=True, target=kwargs["target"])

        label = self.endpoint._eval(locals, eval=False)

        _, d_type = locals[label]
        
        # If assign on Prefix / Struct; then override function
        if not d_type.type in ['LIST']:
            if not Typing.compare(locals[label], target):
                raise TypeError(
                    "Unable to assign type TODO to {label}. (Line {self.token.linepos})")

        # Only value is updated - type remains intact
        locals[label] = [target, d_type]
        return [label, target, d_type._eval(env)]