# ----------------------------------------------------------------------
# while.py
#
# While (statement)
# ----------------------------------------------------------------------

from core.nodes.__base__ import Statement

class While(Statement):
    def __init__(self, condition, block) -> None:
        super().__init__()

        self.condition, self.block = condition, block

    def __str__(self) -> str:
        return f"While <{self.condition}> [{self.block}]"

    def _eval(self, env, debug = True):        
        while self.condition._eval(env):
            self.block._eval(env, debug)