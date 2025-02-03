from __future__ import annotations

from .draw import Draw
from .node import Node
from .connector import Connector

import numpy as np


class Circle(Draw):

    def __init__(self, point: np.ndarray | str | Node, radius: float, **options):
        self.radius = radius
        self.center = point

        super().__init__([point, str(radius)], connector=Connector("circle"), **options)

    # Override how points work
    @property
    def points(self) -> list[np.ndarray | str]:
        return [self.center, str(self.radius)]

    @points.setter
    def points(self, p):
        pass
