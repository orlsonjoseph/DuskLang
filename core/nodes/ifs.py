# ----------------------------------------------------------------------
# if.py
#
# If (statement)
# ----------------------------------------------------------------------

from core.nodes.__base__ import Statement

class If(Statement):
    def __init__(self, condition, block, else_block = None) -> None:
        super().__init__()

        self.condition, self.block = condition, block
        self.else_block = else_block

    def __str__(self) -> str:
        return f"If <{self.condition}> [{self.block}] ELSE {self.else_block}"

    def _eval(self, env, debug = True):        
        to_execute = self.block if self.condition._eval(env) else self.else_block

        if to_execute is not None: to_execute._eval(env, debug)
        