# ----------------------------------------------------------------------
# token.py
#
# Token object
# ----------------------------------------------------------------------

class Token:
    def __init__(self, type, value, pos) -> None:
        self.type = type.split('_')[-1]
        self.value = value

        self.linepos, self.charpos = pos

    def __str__(self) -> str:
        return f"({self.type}, {self.value})"

    def __repr__(self) -> str:
        return self.__str__()
    
    # Overloading comparison
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, str):
            return self.type == __o

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
