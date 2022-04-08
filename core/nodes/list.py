# ----------------------------------------------------------------------
# List.py
#
# List
# ----------------------------------------------------------------------

from core.nodes.__base__ import Expression, Statement

from core.resources.exceptions import NameError, TypeError
from core.resources.typing import Typing

class List(Expression):
    def __init__(self, value, token) -> None:
        super().__init__()

        self.value, self.token = value, token

    def __str__(self) -> str:
        return f"List <{self.value}>"

    def _eval(self, env, **kwargs):
        super()._eval(env)

        return [v._eval(env, eval = True) for v in self.value]

class Indexing(Statement):
    def __init__(self, name, index, token) -> None:
        super().__init__()

        self.name, self.index = name, index

        self.token = token

    def __str__(self) -> str:
        return f"Indexing [{self.name}, {self.index}]"

    def _eval(self, env, **kwargs):
        label, index = self.name._eval(env, eval = False), self.index._eval(env)

        # Type checking
        _, d_type = env[label]
        if d_type.type not in ['LIST']:
            raise TypeError(
                f"Indexing operation applies only to List. (Line {self.token.linepos})")

        if Typing.type_of(index) is not 'int':
            raise TypeError(
                f"List indices must be integers. (Line {self.token.linepos})")   

        array = self.name._eval(env)
        if index >= len(array):
            raise IndexError(
                f"List index out of range. (Line {self.token.linepos})")
        
        # If eval then reassign
        if "eval" in kwargs and kwargs["eval"]:
            array[index] = kwargs["target"]._eval(env, eval = True)

        return array[index]
        