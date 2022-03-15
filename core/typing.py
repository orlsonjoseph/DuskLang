# ----------------------------------------------------------------------
# typing.py
#
# Typing
# ----------------------------------------------------------------------

from core.ast.base import Expression

class Typing:
    def type_of(var):
        if isinstance(var, list):
            _, d_type = var

            if isinstance(d_type, Expression) and hasattr(d_type, 'type'):
                return d_type.type.lower()
        
        if isinstance(var, int):
            return 'int'
        
        if isinstance(var, float):
            return 'float'

        if isinstance(var, str):
            return 'str'

        return None

    def compare(var_a, var_b):
        return Typing.type_of(var_a) == Typing.type_of(var_b)
