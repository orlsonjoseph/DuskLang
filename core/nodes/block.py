# ----------------------------------------------------------------------
# block.py
#
# Block
# ----------------------------------------------------------------------

from core.nodes.__base__ import Statement

class Block(Statement):
    def __init__(self, body) -> None:
        super().__init__()

        self.body = body
    
    def __str__(self) -> str:
        return f"Block - {self.body}"