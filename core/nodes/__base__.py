# ----------------------------------------------------------------------
# __base__.py
#
# Base: Module level objects
# ----------------------------------------------------------------------

class Node:
    def __repr__(self) -> str:
        return self.__str__()        

    def _eval(self, env):
        pass

class Statement(Node):
    pass

class Expression(Node):
    pass