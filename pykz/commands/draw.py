from __future__ import annotations

from ..command import Command
from .node import Node
from ..formatting import format_vector
import numpy as np
from typing import Iterable
from .connector import Connector


class Draw(Command):

    def __init__(self,
                 points: Iterable[np.ndarray | str | Node],
                 connector: Connector,
                 **options,
                 ):
        self.points = points
        self._connector = connector
        super().__init__("draw", **options)

    def _format_pt(self, pt: np.ndarray | str | Node) -> str:
        if isinstance(pt, Node):
            return f"{pt.name}"
        if isinstance(pt, (str, float)):
            return f"{pt}"
        return format_vector(pt, ", ")

    def _format_middle(self) -> str:
        formatted_pts = [f"({self._format_pt(p)})" for p in self.points]
        connector_str = self._connector.get_code()
        return connector_str.join(formatted_pts)
