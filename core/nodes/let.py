# ----------------------------------------------------------------------
# let.py
#
# Let (statement)
# ----------------------------------------------------------------------

from core.nodes.__base__ import Statement

from core.resources.exceptions import NameError

class Let(Statement):
    def __init__(self, label, type, value) -> None:
        super().__init__()

        self.label, self.type = label, type
        self.value = value

    def __str__(self) -> str:
        return f"Let [{self.label}] {self.type} {self.value}"

    def _eval(self, env):
        super()._eval(env)

        if self.label.name in env:
            raise NameError(
                f"Name {self.label} already exists. (Line {self.label.linepos}")
        
        type = self.type._eval(env)
        
        # TODO single assignment to arrays
        if type in ['ARRAY'] and isinstance(self.value, list):
            value = [v._eval(env) for v in self.value]
        else:
            value = self.value._eval(env)

        env[self.label.name] = [value, self.type]
        return (self.label.name, value, type)