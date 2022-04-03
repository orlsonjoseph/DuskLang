# ----------------------------------------------------------------------
# let.py
#
# Let (statement)
# ----------------------------------------------------------------------

from core.nodes.__base__ import Statement

from core.resources.exceptions import NameError

class Let(Statement):
    def __init__(self, name, type, token) -> None:
        super().__init__()

        self.name, self.type = name, type
        self.token = token

    def __str__(self) -> str:
        return f"Let [{self.name}] {self.type}]"

    def _eval(self, env, **kwargs):
        super()._eval(env)

        label = self.name._eval(env, eval = False)

        if label in env:
            raise NameError(
                f"Name {label} already exists. (Line {self.token.linepos}")
        
        env[label] = [None, self.type]
        return label