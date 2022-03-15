# ----------------------------------------------------------------------
# typing.py
#
# Typing
# ----------------------------------------------------------------------

from core.ast.base import Expression

class Typing:
    def type_of(var):
        if isinstance(var, tuple):
            _, d_type = var

            if isinstance(d_type, Expression) and hasattr(d_type, 'type'):
                return d_type.type.lower()
        
        if isinstance(var, int):
            return 'int'

        return None

    def compare(var_a, var_b):
        return Typing.type_of(var_a) == Typing.type_of(var_b)
