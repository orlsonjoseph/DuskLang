# ----------------------------------------------------------------------
# eval.py
#
# Eval
# ----------------------------------------------------------------------

class Eval:
    def __init__(self, ast, debug = False) -> None:
        # Env that holds defined variables and values
        self.environment = {}

        # Abstract syntaxic tree of the program to be evaluated
        self.ast = ast

        # Debug state
        self.debug = debug

    def decorate(self):
        """
        Decorates the given AST through multiple optimizations passes

        Returns:
            ast Program: decorated AST
        """
        return self.ast

    def run(self):
        self.ast = self.decorate()

        for i, statement in enumerate(self.ast.body):
            output = statement._eval(self.environment)

            if self.debug:
                print(f"STMT[{i}] > {output}")
