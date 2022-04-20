# ----------------------------------------------------------------------
# system.py
#
# Dusk System Utilities
# ----------------------------------------------------------------------

from core.nodes.typeid import TypeId

builtin_type = TypeId('builtin')

SYSTEM = {
    # System variables
    '__version__': [0.1, TypeId('float')],
    # __file__
    # __name__

    # System functions
    'abs'       : [abs,     builtin_type],
    'bin'       : [bin,     builtin_type],
    'chr'       : [chr,     builtin_type],
    'hash'      : [hash,    builtin_type],
    'hex'       : [hex,     builtin_type],
    'ord'       : [ord,     builtin_type],
    'gets'      : [input,   builtin_type],
    'sizeof'    : [len,     builtin_type],
    'oct'       : [oct,     builtin_type],
    'puts'      : [print,   builtin_type],
    'sort'      : [sorted,  builtin_type],

    # List functions
    # append
    # extend
    # index
    # insert
    # pop
}