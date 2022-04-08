# ----------------------------------------------------------------------
# program.py
#
# Program
# ----------------------------------------------------------------------

from core.nodes.__base__ import Statement

class Program(Statement):
    def __init__(self, body) -> None:
        super().__init__()

        self.body = body

    def __str__(self) -> str:
        return f"Program - {self.body}"
    
    def _eval(self, env, debug = False):
        for i, statement in enumerate(self.body):
            output = statement._eval(env)

            if debug:
                print(f"STMT[{i}] > {output}")