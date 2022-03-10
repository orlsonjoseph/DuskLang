# ----------------------------------------------------------------------
# ast.py
#
# Abstract Syntactic Tree
# ----------------------------------------------------------------------

class Node:
    def __repr__(self) -> str:
        return self.__str__()        

    def _eval(self, env, **kwargs):
        pass

class Statement(Node):
    pass

class Expression(Node):
    pass