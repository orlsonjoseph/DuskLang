# ----------------------------------------------------------------------
# block.py
#
# Block
# ----------------------------------------------------------------------

from core.nodes.__base__ import Statement

class Block(Statement):
    def __init__(self, body) -> None:
        super().__init__()

        self.body = body
    
    def __str__(self) -> str:
        return f"Block - {self.body}"

    def _eval(self, env, debug = False, **kwargs):        
        # TODO locals apply only to functions
        for i, statement in enumerate(self.body):
            output = statement._eval(env, eval=True)

            if debug:
                print(f"\tSTMT[{i}] > {output}")

        return 