from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from ..environment import Environment
from ..util import format_list


@dataclass
class View:
    azimuth: int
    elevation: int

    def __str__(self) -> str:
        return f"{{{self.azimuth}}}{{{self.elevation}}}"


class AxisMode(Enum):
    normal = "normal"
    linear = "linear"
    log = "log"


class AxisDir(Enum):
    normal = "normal"
    reverse = "reverse"


class Grid(Enum):
    minor = "minor"
    major = "major"
    both = "both"
    none = "none"


class Axis(Environment):

    def __init__(self,
                 xlabel: str | None = None,
                 ylabel: str | None = None,
                 view: View | None = None,
                 width: str | None = None,
                 height: str | None = None,
                 scale_only_axis: bool = False,
                 axis_x_line: str | None = None,
                 axis_y_line: str | None = None,
                 axis_z_line: str | None = None,
                 xmode: AxisMode | None = None,
                 ymode: AxisMode | None = None,
                 zmode: AxisMode | None = None,
                 x_dir: AxisDir | None = None,
                 y_dir: AxisDir | None = None,
                 z_dir: AxisDir | None = None,
                 axis_equal: bool = False,
                 axis_equal_image: bool = False,
                 xmin: float | None = None, xmax: float | None = None,
                 ymin: float | None = None, ymax: float | None = None,
                 zmin: float | None = None, zmax: float | None = None,
                 grid: Grid | None = None,
                 xminorgrids: bool | None = None,
                 yminorgrids: bool | None = None,
                 zminorgrids: bool | None = None,
                 xmajorgrids: bool | None = None,
                 ymajorgrids: bool | None = None,
                 zmajorgrids: bool | None = None,
                 xtick: str | None = None,
                 ytick: str | None = None,
                 ztick: str | None = None,
                 **extra
                 ):
        arguments = locals()
        arguments.pop("extra")
        arguments.pop("self")
        arguments.pop("__class__")
        arguments = {key.replace("_", " "): value for (key, value) in arguments.items()
                     if value is not None
                     }
        super().__init__("axis", **arguments, **extra)

    def set_xlabel(self, label: str):
        self.set_option("xlabel", label)

    def enlarge_limits(self, amount: float = 0.05, direction: str | None = None):
        """Enlarge the range of axes (only x or y if `direction` is provided).

        Adds the `enlarge x limits` option.

        Arguments:
            - amount: fraction by which to increase the size of the axes. The final range will be `(1 + amount) * original_length`
            - direction: "x" | "y". If provided, only apply to the corresponding axis.
        """
        allowed_dirs = ["x", "y", None]
        if direction not in allowed_dirs:
            raise ValueError(f"Expected direction to belong to {allowed_dirs}. Got {direction}")

        if direction:
            self.set_option(f"enlarge {direction} limits", amount)
        else:
            self.set_option("enlarge x limits", amount)
            self.set_option("enlarge y limits", amount)

    # def extend_axis_lines(self, amount: int | str = "10pt"):
    #     self.set_option("axis line style", Options(
    #         **{"shorten >": "-10pt", "shorten <": "-10pt"}
    #     ))

    def set_ylabel(self, label: str):
        self.options.set_option("ylabel", label)

    def set_zlabel(self, label: str):
        self.options.set_option("zlabel", label)

    def set_xlims(self, lims: tuple[float]):
        (self.options["xmin"], self.options["xmax"]) = lims

    def set_ylims(self, lims: tuple[float]):
        (self.options["ymin"], self.options["ymax"]) = lims

    def set_zlims(self, lims: tuple[float]):
        (self.options["zmin"], self.options["zmax"]) = lims

    def get_ylims(self) -> tuple:
        return (self.options.get("ymin", -1), self.options.get("ymax", 1))

    def center(self):
        """Center the axis lines"""
        self.set_option("axis lines", "center")

    def set_axis_label_position(self, axis: str, position: str):
        """Set label position of the given axis relative to the arrowhead.
        As a side-effect, it also centers the axes.

        Arguments:
            - axis [str]: "x", "y" or "z"
            - positions [str]: "left", "right", "above", "below"
        """
        axis = axis.lower()
        position = position.lower()
        known_axes = ("x", "y", "z")
        known_positions = ("left", "right", "above", "below")

        if axis not in known_axes:
            raise ValueError(f"Expected axis in {known_axes}. Got {axis}.")

        if position not in known_positions:
            raise ValueError(f"Expected position in {known_positions}. Got {position}.")

        self.center()
        anchors = dict(
            above="south",
            below="north",
            left="east",
            right="west"
        )

        self.update_option(f"{axis} label style", "anchor", anchors[position])

    def boxed(self):
        self.set_option("axis lines", "box")

    def _set_ticks(self, values: tuple[float], labels: tuple[str] | None, direction: str):
        self.set_option(f"{direction}tick", f"{{{format_list(values)}}}")
        if labels is not None:
            self.set_option(f"{direction}ticklabels", f"{{{format_list(labels)}}}")

    def set_yticks(self, values: tuple[float], labels: tuple[str] | None = None):
        self._set_ticks(values, labels, "y")

    def set_xticks(self, values: tuple[float], labels: tuple[str] | None = None):
        self._set_ticks(values, labels, "x")

    def set_zticks(self, values: tuple[float], labels: tuple[str] | None = None):
        self._set_ticks(values, labels, "z")

    def set_xmax(self, v):
        self.options["xmax"] = v

    def set_ymax(self, v):
        self.options["ymax"] = v

    def set_zmax(self, v):
        self.options["zmax"] = v

    def set_xmin(self, v):
        self.options["xmin"] = v

    def set_ymin(self, v):
        self.options["ymin"] = v

    def set_zmin(self, v):
        self.options["zmin"] = v
