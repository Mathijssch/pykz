from .tikzcode import Tex
from .util import format_list


class Calc(Tex):
    """Class to represent a calc-coordinate"""

    def __init__(self, point: str | Tex, offset: tuple[float] | str):
        self._pt = point
        self._offset = offset

    def _format_offset(self) -> str:
        if isinstance(self._offset, str):
            return self._offset
        return f"({format_list(self._offset)})"

    def get_code(self) -> str:
        return f"$({self._pt}) + {self._format_offset()}$"
