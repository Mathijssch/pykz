import contourpy
import numpy as np
from .tikzcode import TikzCode, Tex
from .plot import create_plot, Addplot
from .formatting import format_matrix

PointArray = np.ndarray  # a n x 2 array of points
IndexArray = np.ndarray  # a n-array of indices


class ContourFilled(TikzCode):
    def __init__(
        self,
        point_list: PointArray,
        indices: IndexArray,
        relative_level: int,
        **plot_options,
    ):
        super().__init__()
        self.point_list = point_list
        self.indices = indices
        self.level = relative_level
        self._options = dict(draw="none", fill=True)
        # if ("draw" not in plot_options) and ("fill" not in plot_options):
        self._options["color of colormap"] = self.level
        self._options.update(plot_options)
        self.build_lines()

    @property
    def plot_commands(self) -> list[Addplot]:
        return self.lines

    @property
    def outer_contour(self) -> PointArray:
        return self.point_list[self.indices[0] : self.indices[1]]

    def build_lines(self):
        formatted_lines = [
            format_matrix(self.point_list[s:e], row_sep=r"\\")
            for s, e in zip(self.indices[:-1], self.indices[1:])
        ]
        full_cycle = "\nnan nan\\\\\n".join(formatted_lines)
        plot_cmd = Addplot(full_cycle, **self._options)
        self.add_line(plot_cmd)


class Contour(TikzCode):
    def __init__(self, point_list: list[PointArray], relative_level: int, **options):
        super().__init__()
        self.point_list = point_list
        self.level = relative_level

        self._options = dict(draw=True, fill="none")
        if ("draw" not in options) and ("fill" not in options):
            self._options["color of colormap"] = self.level
        self._options.update(options)
        self.build_lines()

    @property
    def outer_contour(self) -> PointArray:
        return self.point_list

    @property
    def plot_commands(self) -> list[Addplot]:
        return self.lines

    def build_lines(self):
        for line in self.point_list:
            self.add_line(self.create_plot_command(line))

    def create_plot_command(self, line: PointArray):
        plot_cmd = create_plot(line[:, 0], line[:, 1], None, **self._options)[0]
        return plot_cmd


def _default_levels(z: np.ndarray, n_levels=10):
    zmin = z.min()
    zmax = z.max()
    return np.linspace(zmin, zmax, n_levels)


def get_relative_level(level, levels):
    from .util import get_extremes_safely

    lower, upper = get_extremes_safely(levels)
    if upper == lower:
        return 500
    return round((level - lower) / (upper - lower) * 1000)


def create_contourf(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    levels: list[float] = None,
    contour_options: dict | None = None,
    **pgfplots_options,
) -> list[ContourFilled]:
    options = dict(fill_type=contourpy.FillType.OuterOffset)
    if contour_options is not None:
        options.update(contour_options)
    generator = contourpy.contour_generator(x, y, z, **options)
    levels = _default_levels(z) if levels is None else levels
    contour_tex = []
    for l1, l2 in zip(levels[:-1], levels[1:]):
        points, indices = generator.filled(l1, l2)
        relative_level = get_relative_level(l1, levels)
        contour_tex.extend(
            [
                ContourFilled(pts, indx, relative_level, **pgfplots_options)
                for pts, indx in zip(points, indices)
            ]
        )
    return contour_tex, levels


def create_contour(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    levels: list[float] = None,
    contour_options: dict | None = None,
    **pgfplots_options,
):
    options = dict(fill_type=contourpy.FillType.OuterOffset)
    if contour_options is not None:
        options.update(contour_options)
    generator = contourpy.contour_generator(
        x, y, z, line_type=contourpy.LineType.Separate, **options
    )
    levels = _default_levels(z) if levels is None else levels
    points = generator.multi_lines(levels)
    contour_tex = [
        Contour(pts, get_relative_level(level, levels), **pgfplots_options)
        for pts, level in zip(points, levels)
    ]
    return contour_tex, levels
