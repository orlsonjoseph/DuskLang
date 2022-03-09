# ----------------------------------------------------------------------
# ast.py
#
# Abstract Syntactic Tree
# ----------------------------------------------------------------------

class Node:
    def __repr__(self) -> str:
        self.__str__()        

    def _eval(self):
        pass

class Statement(Node):
    pass

class Expression(Node):
    pass