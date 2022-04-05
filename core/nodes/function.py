# ----------------------------------------------------------------------
# function.py
#
# Function
# ----------------------------------------------------------------------

from core.nodes.__base__ import Expression, Statement
from core.nodes.typeid import TypeId

# Function Definition
class Function(Statement):
    def __init__(self, name, parameters, block, token) -> None:
        super().__init__()

        self.name, self.parameters = name, parameters

        self.block = block
        self.token = token

    def __str__(self) -> str:
        return f"Function {self.name} > [{self.parameters}] [{self.block}]"

    def _eval(self, env, debug=True):
        super()._eval(env)
        
        name = self.name._eval(env, eval=False)

        locals = {'__body__': self.block}

        if self.parameters is not None: 
            for p in self.parameters: p._eval(locals, eval=True) 

        env[name] = [locals, TypeId('function')]
        return [name, locals]
        
# Return Statement
class Return(Expression):
    def __init__(self, expr, token) -> None:
        super().__init__()

        self.expression, self.token = expr, token

    def __str__(self) -> str:
        return f"Return [{self.expression}]"

    def _eval(self, env, **kwargs):
        super()._eval(env)

        return self.expression._eval(env)

# Function Call
class Call(Expression):
    def __init__(self, name, parameters, token) -> None:
        super().__init__()

        self.name, self.token = name, token
        self.parameters = parameters
        
    def __str__(self) -> str:
        return f"Call {self.name}"

    def _eval(self, env, debug=True):
        super()._eval(env)

        return f"Call {self.name}"