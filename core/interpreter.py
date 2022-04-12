# ----------------------------------------------------------------------
# interpreter.py
#
# Interpreter
# ----------------------------------------------------------------------

from core.builtins.system import SYSTEM

class Interpreter:
    def __init__(self, ast, env, **kwargs) -> None:
        self.ast = ast
        self.env = env

        if "debug" in kwargs:
            self.debug = kwargs["debug"]

    def evaluate(self):
        # Extend environment with builtins
        self.env.update(SYSTEM)

        self.ast._eval(self.env)
