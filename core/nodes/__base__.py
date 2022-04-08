# ----------------------------------------------------------------------
# __base__.py
#
# Base: Module level objects
# ----------------------------------------------------------------------

class Node:
    def __repr__(self) -> str:
        return self.__str__()

class Statement(Node):
    pass

class Expression(Node):
    pass