from __future__ import annotations

from ..command import Command
from ..label import Label
from ..tikzcode import Tex
from ..formatting import format_vector
# from ..options import Options
import numpy as np


class Node(Command):

    def __init__(self,
                 label: str = "",
                 name: str = None,
                 position: np.ndarray | Tex | str = None,
                 label_loc: str = None,
                 axis_coords: bool = False,
                 **options,
                 ):
        self.set_position(position)
        self.axis_coords = axis_coords
        self.label = Label(label)
        if label_loc:
            self.set_label_loc(label_loc)
        # self._label_opts = Options()
        self.name = name
        super().__init__("node", label)
        self.set_options(**options)

    def customize_label(self, **options):
        """Customize the options of the inline label"""
        self.label.set_options(**options)

    # def format_label(self) -> str:

    def set_label_loc(self, loc: str):
        self.label.set_location(loc)

    def set_position(self, position: str | Tex | np.ndarray):
        if isinstance(position, str):
            position = Tex(position)
        if not isinstance(position, Tex) and \
                position is not None:
            position = np.array(position)
        self._position = position

    def _format_middle(self) -> str:
        if self._position is None:
            return ""
        coords = ""
        if isinstance(self._position, np.ndarray):
            coords = format_vector(self._position, separator=", ")
            if self.axis_coords:
                coords = "axis cs: " + coords
        elif isinstance(self._position, Tex):
            coords = self._position.get_code()
        else:
            raise TypeError(
                f"Got unexpected type `{type(self._position)}` for the position of a node."
            )
        middle = ""
        if self.name:
            middle += f"({self.name})"
        if coords:
            middle += f" at ({coords})"
        return middle

    def get_code(self):
        # if self._label_loc is not None:
        if len(self.label.options) > 0:
            self._arguments.clear()  # Remove the label as an argument.
            self.add_argument("")    # Replace it with the empty string, because a node needs a (potentially empty) label text.
            self.set_option("label", self.label.get_code())
        return super().get_code()
