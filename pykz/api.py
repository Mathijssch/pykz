"""Public API"""

from __future__ import annotations

from .tikzcode import TikzCode
from .environments.axis import Axis
from .environments.tikzpicture import TikzPicture
from .commands.addplot import Addplot
from .commands.fillbetween import FillBetween
from .commands.node import Node
from .commands.draw import Draw
from .commands.circle import Circle
from .calc import Calc
from .plot import create_plot, create_surface_plot
from .contour import create_contour, create_contourf, ContourFilled, Contour
import numpy as np
from typing import Optional, Union
from pathlib import Path


class WorkSpace:
    __currfig = None
    __currax = None

    @classmethod
    def scf(cls, fig: TikzPicture):
        cls.__currfig = fig

    @classmethod
    def sca(cls, ax: TikzPicture):
        cls.__currax = ax

    @classmethod
    def gcf(cls) -> Optional[Axis]:
        return cls.__currfig

    @classmethod
    def gca(cls) -> Optional[Axis]:
        return cls.__currax


def gcf() -> Optional[TikzPicture]:
    """
    Get the currently active figure in the workspace, which could be None.
    If you want to create a new one if there is no current figure, then use `figure()`

    Returns
    -------
    Optional[TikzPicture]
        The currently active Figure if there is one.
    """
    return WorkSpace.gcf()


def gca() -> Optional[Axis]:
    """
    Get the currently active axis (representing a pgfplots ``axis``) if there is one.

    If you want to create a new axis in case there is none, then use the `ax()` function.

    Returns
    -------
    Optional[Axis]
        The currently active axis if there is one.
    """
    return WorkSpace.gca()


def __get_or_create_fig() -> TikzPicture:
    f = gcf()
    return f if f is not None else figure()


def __get_or_create_ax() -> Axis:
    a = gca()
    return a if a is not None else ax()


def figure(standalone: bool = True, **options) -> TikzPicture:
    """
    Create a new TikzPicture and set it as the current figure.

    Parameters
    ----------
    standalone : bool, optional
        Whether the figure should be a standalone document, by default True
    **options
        Additional options to pass to the TikzPicture

    Returns
    -------
    TikzPicture
        The newly created figure
    """
    pic = TikzPicture(standalone, **options)
    WorkSpace.sca(None)
    WorkSpace.scf(pic)
    return pic


def ax(**options) -> Axis:
    """
    Create a new Axis object and add it to the current figure.

    Parameters
    ----------
    **options
        Options to pass to the Axis constructor

    Returns
    -------
    Axis
        The newly created axis
    """
    ax = Axis(**options)
    fig = __get_or_create_fig()
    WorkSpace.sca(ax)
    fig.add_axis(ax)
    return ax


def dumps(fig: TikzPicture | None = None) -> str:
    """
    Dump the tex-code of the current figure to a string.

    If no figure is given, the active figure is selected,
    and the contents of this figure are returned.

    Parameters
    ----------
    fig
        Figure to generate the code for. If None is given, then the current figure is used.

    Returns
    -------
    str
        The tex code.
    """
    fig = gcf() if fig is None else fig
    if fig is None:
        return ""
    return fig.get_code()


def preview(fig: TikzPicture | None = None):
    """
    Preview the current figure.

    The contents of this figure are written to a temporary file,
    compiled to a pdf and then opened in the default viewer.
    After the process terminates, these files are removed.

    Parameters
    ----------
    fig : TikzPicture, optional
        The figure to preview. If None is given, the current figure is used.
    """
    fig = gcf() if fig is None else fig
    if fig is None:
        return
    fig.preview()


def save(
    filename: str | Path, fig: TikzPicture | None = None, standalone: bool = False
):
    """
    Save the generated Tikz code to a file.

    Parameters
    ----------
    filename : str | Path
        The path to write the figure to.
        If the extension `.tex` or `.tikz` is not present, `.tex` is appended.
    fig : TikzPicture, optional
        The figure to save. If None is given, the current figure is used.
    standalone : bool, optional
        Whether to save as a standalone document, by default False
    """
    fig = gcf() if fig is None else fig
    if fig is None:
        return
    fig.standalone = standalone
    return fig.export(filename)


def xlabel(lab: str):
    """
    Set the x label of the current axis.

    Parameters
    ----------
    lab : str
        Label text
    """
    ax = __get_or_create_ax()
    ax.set_xlabel(lab)


def xticks(ticks: np.ndarray, labels: list[str] | None = None, ax: Axis | None = None):
    """
    Set the x ticks and optionally label them.

    Parameters
    ----------
    ticks : np.ndarray
        x-coordinates to add ticks at
    labels : list[str], optional
        Labels of the ticks
    ax : Axis, optional
        The axis to modify. The current axes is used if None is passed.
    """
    ax = __get_or_create_ax() if ax is None else ax
    ax.set_xticks(ticks, labels)


def yticks(ticks: np.ndarray, labels: list[str] | None = None, ax: Axis | None = None):
    """
    Set the y ticks and optionally label them.

    Parameters
    ----------
    ticks : np.ndarray
        y-coordinates to add ticks at
    labels : list[str], optional
        Labels of the ticks
    ax : Axis, optional
        The axis to modify. The current axes is used if None is passed.
    """
    ax = __get_or_create_ax() if ax is None else ax
    ax.set_yticks(ticks, labels)


def zticks(ticks: np.ndarray, labels: list[str] | None = None, ax: Axis | None = None):
    """
    Set the z ticks and optionally label them.

    Parameters
    ----------
    ticks : np.ndarray
        z-coordinates to add ticks at
    labels : list[str], optional
        Labels of the ticks
    ax : Axis, optional
        The axis to modify. The current axes is used if None is passed.
    """
    ax = __get_or_create_ax() if ax is None else ax
    ax.set_zticks(ticks, labels)


def usepackage(package_name: str, fig: TikzPicture | None = None, **options):
    """
    Add a usepackage statement to the current or given figure.

    Parameters
    ----------
    name : str
        Name of the style to define
    fig : TikzPicture, optional
        Figure to include the package in. If None, uses current figure.
    **options
        Style options to set
    """
    fig = __get_or_create_fig() if fig is None else fig
    fig.usepackage(package_name, **options)


def usepgfplotslibrary(library_name: str, fig: TikzPicture | None = None, **options):
    """
    Add a usepgfplotslibrary-statement to the current or given figure.

    Parameters
    ----------
    library_name : str
        Name of the library to import
    fig : TikzPicture, optional
        Figure to include the package in. If None, uses current figure.
    **options
        Style options to set
    """
    fig = __get_or_create_fig() if fig is None else fig
    fig.usepgfplotslibrary(library_name, **options)


def usetikzlibrary(library_name: str, fig: TikzPicture | None = None, **options):
    """
    Add a usetikzlibrary-statement to the current or given figure.

    Parameters
    ----------
    library_name : str
        Name of the library to import
    fig : TikzPicture, optional
        Figure to include the package in. If None, uses current figure.
    **options
        Style options to set
    """
    fig = __get_or_create_fig() if fig is None else fig
    fig.preamble.usetikzlibrary(library_name, **options)


def newcommand(
    name: str, implementation: str, n_args: int = 0, fig: TikzPicture | None = None
):
    """
    Define a new command for the figure.

    Parameters
    ----------
    name : str
        Name of the command to define
    implementation: str
        String to use as the implementation of the new command
    fig : TikzPicture, optional
        Figure to define the style for. If None, uses current figure.
    """
    fig = __get_or_create_fig() if fig is None else fig
    fig.preamble.newcommand(name, implementation, n_args)


def define_style(name: str, fig: TikzPicture | None = None, **options):
    """
    Define a new style for the figure.

    Parameters
    ----------
    name : str
        Name of the style to define
    fig : TikzPicture, optional
        Figure to define the style for. If None, uses current figure.
    **options
        Style options to set
    """
    fig = __get_or_create_fig() if fig is None else fig
    fig.set_style(name, **options)


def calc(pt: str, offset: tuple[float] | str, fig: TikzPicture | None = None) -> Calc:
    usetikzlibrary("calc", fig)
    calc = Calc(pt, offset)
    return calc


def ylabel(lab: str):
    """
    Set the y label of the current axis.

    Parameters
    ----------
    lab : str
        Label text
    """
    ax = __get_or_create_ax()
    ax.set_ylabel(lab)


def zlabel(lab: str):
    """
    Set the z label of the current axis.

    Parameters
    ----------
    lab : str
        Label text
    """
    ax = __get_or_create_ax()
    ax.set_zlabel(lab)


def xlim(limits: tuple[float]):
    """
    Set the x limits of the current axis.

    Parameters
    ----------
    limits : tuple[float]
        Tuple containing (min, max) limits
    """
    ax = __get_or_create_ax()
    ax.set_xlims(limits)


def ylim(limits: tuple[float]):
    """
    Set the y limits of the current axis.

    Parameters
    ----------
    limits : tuple[float]
        Tuple containing (min, max) limits
    """
    ax = __get_or_create_ax()
    ax.set_ylims(limits)


def axhline(y: float, ax: Axis | None = None, **options) -> list[Addplot]:
    """
    Plot a horizontal line at the provided y value.

    Parameters
    ----------
    y : float
        y-coordinate of the line
    ax : Axis, optional
        Axis to add the line to. If None, uses current axis.
    **options
        Additional plotting options

    Returns
    -------
    list[Addplot]
        List of plot commands created
    """
    ax = __get_or_create_ax() if ax is None else ax
    xlims = ax.get_xlims()
    return plot(xlims, [y, y], ax=ax, **options)


def scale(scale: float, fig: TikzPicture | None = None):
    """
    Set the scale of the figure.

    Parameters
    ----------
    scale : float
        Scale factor
    fig : TikzPicture, optional
        Figure to scale. If None, uses current figure.
    """
    fig = gcf() if fig is None else fig
    fig.set_option("scale", scale)


def point(
    coordinates: np.ndarray | None = None,
    label: str = "",
    name: str | None = None,
    axis_coords: bool | None = None,
    label_loc: str = "above",
    size: int | str = "1pt",
    axis: Axis | None = None,
    fig: TikzPicture | None = None,
    **options,
) -> Node:
    """
    Draw a point at the given coordinates.

    It creates a node, but also adds some styling to make it look like a point.

    See also: node()

    Parameters
    ----------
    coordinates : np.ndarray, optional
        Position of the point
    label : str, optional
        Label text, by default ""
    name : str, optional
        Name of the node
    axis_coords : bool, optional
        Whether to use axis coordinates
    label_loc : str, optional
        Label location ("above", "below", "right", "left"), by default "above"
    size : int | str, optional
        Size of the point, by default "1pt"
    axis : Axis, optional
        Axis to add the point to
    fig : TikzPicture, optional
        Figure to add the point to
    **options
        Additional styling options

    Returns
    -------
    Node
        The created node object
    """
    options["pt"] = True
    nd = node(coordinates, label, name, axis_coords, label_loc, axis, fig, **options)
    fig = fig if fig is not None else __get_or_create_fig()
    fig.define_style("pt", inner_sep=size, circle=True, fill=True)
    return nd


def node(
    coordinates: np.ndarray | None = None,
    label: str = "",
    name: str = "",
    axis_coords: bool | None = None,
    label_loc: str | None = None,
    axis: Axis | None = None,
    fig: TikzPicture | None = None,
    **options,
) -> Node:
    """
    Draw a node at the given coordinates.

    Parameters
    ----------
    coordinates : np.ndarray, optional
        Position of the node or name of a previously defined node
    label : str, optional
        Label text
    name : str, optional
        Name of the node
    axis_coords : bool, optional
        Whether to interpret coordinates in axis coordinates
    label_loc : str, optional
        Label location (None, "above", "below", "right", "left" or combinations)
    axis : Axis, optional
        Axis to add the node to
    fig : TikzPicture, optional
        Figure to add the node to
    **options
        Additional styling options

    Returns
    -------
    Node
        The created node object
    """
    if axis_coords is None:
        given_axis = gca() if axis is None else axis
        axis_coords = False if given_axis is None else True

    if not label:
        label_loc = None
    node = Node(label, name, coordinates, label_loc, axis_coords, **options)
    if axis is None and axis_coords:
        axis = __get_or_create_ax()
        axis.add(node)
        return node

    fig = fig if fig is not None else __get_or_create_fig()
    fig.add(node)
    return node


def fill_between(
    x: np.ndarray,
    y1: np.ndarray,
    y2: np.ndarray,
    *,
    draw_options=None,
    fill_options=None,
) -> FillBetween:
    """
    Fill the area between two curves.

    Parameters
    ----------
    x : np.ndarray
        x-coordinates
    y1 : np.ndarray
        y-coordinates of first curve
    y2 : np.ndarray
        y-coordinates of second curve
    draw_options : dict, optional
        Options for drawing the curves
    fill_options : dict, optional
        Options for filling the area

    Returns
    -------
    FillBetween
        The fill between plot command
    """
    ax = __get_or_create_ax()
    ax.add_requirement(r"\usepgfplotslibrary{fillbetween}")

    draw_options = draw_options if draw_options is not None else dict()
    fill_options = fill_options if fill_options is not None else dict()

    draw_options["name path"] = "first"
    plot(x, y1, ax, **draw_options)

    draw_options["name path"] = "second"
    plot(x, y2, ax, **draw_options)[0]

    fill_plot = FillBetween("first", "second", **fill_options)
    ax.add(fill_plot)
    return fill_plot


# def quiver(x: np.ndarray, y: np.ndarray, dx: np.ndarray, dy: np.ndarray, **options) -> Quiver


def axvline(x: float, ax: Axis | None = None, **options) -> list[Addplot]:
    """
    Plot a vertical line at the provided x value.

    Parameters
    ----------
    x : float
        x-coordinate of the line
    ax : Axis, optional
        Axis to add the line to. If None, uses current axis.
    **options
        Additional plotting options

    Returns
    -------
    list[Addplot]
        List of plot commands created
    """  # TODO: Think of ways to represent this allow axes dimensions to be updated afterwards.
    ax = ax if ax is not None else __get_or_create_ax()
    ymin, ymax = ax.get_ylims()
    xes = np.array((x, x))
    ys = np.array((ymin, ymax))
    return plot(xes, ys, ax=ax, **options)


Point = Union[np.ndarray, str, Node]


def __create_draw(connector_type: str, points: list[Point], **options) -> Draw:
    from .commands import Connector

    connector = Connector(connector_type)
    draw = Draw(points, connector, **options)
    return draw


def __add_draw_command(draw: Draw) -> Draw:
    fig = __get_or_create_fig()
    fig.add(draw)
    return draw


def __create_and_add_draw(connector_type: str, points: list[Point], **options):
    draw = __create_draw(connector_type, points, **options)
    return __add_draw_command(draw)


def rectangle(c1: Point, c2: Point, **options) -> Draw:
    """
    Draw a rectangle between two points.

    Parameters
    ----------
    c1 : Point
        First corner point
    c2 : Point
        Second corner point
    **options
        Additional drawing options

    Returns
    -------
    Draw
        The drawing command
    """
    return __create_and_add_draw("rectangle", [c1, c2], **options)


def circle(center: Point, radius: float, **options) -> Circle:
    """
    Draw a circle with given center and radius.

    Parameters
    ----------
    center : Point
        Center point of the circle
    radius : float
        Radius of the circle
    **options
        Additional drawing options

    Returns
    -------
    Circle
        The circle drawing command
    """
    circle = Circle(center, radius, **options)
    return __add_draw_command(circle)


def line(points: list[Point], connection: str = "--", **options) -> Draw:
    """
    Draw a line through a list of points.

    Parameters
    ----------
    points : list[Point]
        List of points to connect
    connection : str, optional
        Type of connection between points, by default "--"
    **options
        Additional drawing options

    Returns
    -------
    Draw
        The drawing command
    """
    return __create_and_add_draw(connection, points, **options)


def arrow(
    points: list[Point],
    forward: bool = True,
    backward: bool = False,
    arrowhead: str | None = None,
    **options,
) -> Draw:
    """
    Draw an arrow through a list of points.

    Parameters
    ----------
    points : list[Point]
        List of points to connect
    forward : bool, optional
        Whether to draw forward arrow, by default True
    backward : bool, optional
        Whether to draw backward arrow, by default False
    arrowhead : str, optional
        Style of arrowhead
    **options
        Additional drawing options

    Returns
    -------
    Draw
        The drawing command
    """
    bw = "<" if backward else ""
    fw = ">" if forward else ""
    arrow = bw + "-" + fw if (bw or fw) else "--"
    arrow_opts = {arrow: True}
    if arrowhead is not None:
        if forward:
            arrow_opts[">"] = arrowhead
        if backward:
            arrow_opts["<"] = arrowhead
    options.update(arrow_opts)
    return line(points, **options)


def plot(
    x,
    y=None,
    z=None,
    ax: Axis | None = None,
    label: str | tuple[str] | None = None,
    inline_label: bool = False,
    **options,
) -> list[Addplot]:
    """
    Create a plot command.

    Parameters
    ----------
    x : array-like
        x-coordinates or data
    y : array-like, optional
        y-coordinates
    z : array-like, optional
        z-coordinates for 3D plots
    ax : Axis, optional
        Axis to add the plot to
    label : str | tuple[str], optional
        Label or tuple of labels for the plot
    inline_label : bool, optional
        Whether to place label inline with the plot, by default False
    **options
        Additional plotting options

    Returns
    -------
    list[Addplot]
        List of plot commands created
    """

    ax = ax if ax is not None else __get_or_create_ax()
    plot_commands = create_plot(x, y, z, label, inline_label, **options)
    for plt in plot_commands:
        ax.add(plt)
    return plot_commands


def boxplot(
    lower_whisker: float,
    lower_quartile: float,
    median: float,
    upper_quartile: float,
    upper_whisker: float,
    *,
    position: float = 1,
    width: float = 0.5,
    outliers=None,
    orientation: str = "vertical",
    ax: Axis | None = None,
    label: str | None = None,
    **options,
) -> Addplot:
    """Add a box plot from manually computed statistics.

    Call repeatedly with different positions to compare datasets on one axis.
    Fractional positions and smaller widths allow grouped comparisons.

    Parameters
    ----------
    lower_whisker, upper_whisker : float
        Outer ends of the whiskers.
    lower_quartile, upper_quartile : float
        Lower and upper edges of the box.
    median : float
        Position of the line inside the box. The five statistics must be
        finite and ordered from the lower whisker to the upper whisker.
    position : float, optional
        Position on the categorical axis, by default 1.
    width : float, optional
        Positive box width in categorical-axis units, by default 0.5.
    outliers : array-like, optional
        One-dimensional sequence of finite outlier values.
    orientation : {"vertical", "horizontal"}, optional
        Direction of the values, by default "vertical". For horizontal boxes,
        position and width refer to the y axis.
    ax : Axis, optional
        Target axis. Defaults to the current axis, creating one if needed.
    label : str, optional
        Legend entry. Omit for subsequent boxes of the same method in a group.
    **options
        PGFPlots styling options, such as ``fill``, ``draw``, and ``mark``.

    Returns
    -------
    Addplot
        The added command, whose options can be customized further.

    Notes
    -----
    The PGFPlots statistics library is included automatically. No statistics
    are computed from samples and outliers are supplied explicitly.
    """
    from .commands.boxplot import Boxplot
    from .options import Options

    statistics = np.asarray(
        [lower_whisker, lower_quartile, median, upper_quartile, upper_whisker],
        dtype=float,
    )
    if statistics.shape != (5,) or not np.all(np.isfinite(statistics)):
        raise ValueError("Box plot statistics must be finite scalars.")
    if np.any(np.diff(statistics) < 0):
        raise ValueError("Box plot statistics must be in nondecreasing order.")
    if not np.isfinite(position):
        raise ValueError("position must be finite.")
    if not np.isfinite(width) or width <= 0:
        raise ValueError("width must be finite and positive.")
    if orientation not in ("vertical", "horizontal"):
        raise ValueError("orientation must be 'vertical' or 'horizontal'.")
    outliers = np.asarray([] if outliers is None else outliers, dtype=float)
    if outliers.ndim != 1 or not np.all(np.isfinite(outliers)):
        raise ValueError("outliers must be a one-dimensional finite sequence.")

    opts = Options(**options)
    opts.set_option("boxplot prepared", Options(
        lower_whisker=statistics[0], lower_quartile=statistics[1],
        median=statistics[2], upper_quartile=statistics[3],
        upper_whisker=statistics[4], draw_position=position,
    ))
    opts.set_option("boxplot/draw direction", "y" if orientation == "vertical" else "x")
    opts.set_option("boxplot/box extend", width)
    # Prepared boxes otherwise use their data-sized geometry in the legend.
    if "legend image code/.code" not in opts:
        opts.set_option("area legend", True)
    if label is None and "forget plot" not in opts:
        opts.set_option("forget plot", True)
    command = Boxplot(outliers, label=label, **opts)
    ax = ax if ax is not None else __get_or_create_ax()
    requirement = r"\usepgfplotslibrary{statistics}"
    if requirement not in ax.requirements.get_code().splitlines():
        ax.add_requirement(requirement)
    ax.add(command)
    return command


def grouped_boxplot(
    experiments,
    *,
    experiment_labels=None,
    method_labels=None,
    method_options=None,
    outliers=None,
    group_width: float = 0.8,
    orientation: str = "vertical",
    ax: Axis | None = None,
    **options,
) -> list[list[Addplot]]:
    """Compare methods across experiments using automatically grouped boxes.

    Parameters
    ----------
    experiments : array-like, shape (n_experiments, n_methods, 5)
        Precomputed summaries in the order ``(lower_whisker, lower_quartile,
        median, upper_quartile, upper_whisker)``. Every experiment must contain
        the same nonzero number of methods, in the same order.
    experiment_labels : sequence of str, optional
        One tick label per experiment. Defaults to numbers starting at 1.
    method_labels : sequence of str, optional
        One legend label per method. Each appears only once.
    method_options : sequence of mappings, optional
        Styling options for each method, overriding shared options. For example,
        ``[{"fill": "cyan"}, {"fill": "red"}]``.
    outliers : nested sequence, optional
        Outlier sequences indexed by experiment and method. Each entry may be
        None or an empty sequence when there are no outliers.
    group_width : float, optional
        Total group span in categorical-axis units, by default 0.8. Must be
        greater than zero and at most 1. Methods occupy equally spaced slots;
        each box fills 80 percent of its slot.
    orientation : {"vertical", "horizontal"}, optional
        Direction of the values, by default "vertical".
    ax : Axis, optional
        Target axis, defaulting to the current axis, creating one if needed.
    **options
        Shared PGFPlots styling options. Position, width, and legend inclusion
        are managed by this function.

    Returns
    -------
    list[list[Addplot]]
        Commands indexed by experiment and method, available for customization.

    Notes
    -----
    Groups are centered at 1, 2, ... . Categorical ticks are replaced on the
    target axis (x for vertical boxes, y for horizontal boxes). All inputs are
    validated before modifying the target axis.
    """
    from collections.abc import Mapping
    from .options import Options

    summaries = np.asarray(experiments, dtype=float)
    if (summaries.ndim != 3 or summaries.shape[-1] != 5
            or summaries.shape[0] == 0 or summaries.shape[1] == 0):
        raise ValueError("experiments must have shape (n_experiments, n_methods, 5).")
    n_experiments, n_methods, _ = summaries.shape
    if not np.isscalar(group_width) or not np.isfinite(group_width) or not 0 < group_width <= 1:
        raise ValueError("group_width must be finite, greater than zero, and at most 1.")

    def labels(values, count, name):
        if values is None:
            return None
        if isinstance(values, str):
            raise ValueError(f"{name} must contain {count} strings.")
        values = list(values)
        if len(values) != count or not all(isinstance(value, str) for value in values):
            raise ValueError(f"{name} must contain {count} strings.")
        return values

    experiment_labels = labels(experiment_labels, n_experiments, "experiment_labels")
    if experiment_labels is None:
        experiment_labels = [str(i) for i in range(1, n_experiments + 1)]
    method_labels = labels(method_labels, n_methods, "method_labels")
    styles = [{} for _ in range(n_methods)] if method_options is None else list(method_options)
    if len(styles) != n_methods or not all(isinstance(style, Mapping) for style in styles):
        raise ValueError("method_options must contain one mapping per method.")
    if outliers is None:
        outliers = [[None] * n_methods for _ in range(n_experiments)]
    else:
        outliers = [list(row) for row in outliers]
        if len(outliers) != n_experiments or any(len(row) != n_methods for row in outliers):
            raise ValueError("outliers must contain one sequence per experiment and method.")

    # Build on a detached axis first so even a bad summary or outlier in the
    # last experiment leaves the user's figure and workspace untouched.
    staging = Axis()
    slot = group_width / n_methods
    commands = []
    for i, experiment in enumerate(summaries):
        row = []
        for j, summary in enumerate(experiment):
            style = dict(Options(**options))
            style.update(Options(**styles[j]))
            label = method_labels[j] if method_labels is not None and i == 0 else None
            style["forget plot"] = label is None
            row.append(boxplot(
                *summary,
                position=i + 1 + (j - (n_methods - 1) / 2) * slot,
                width=0.8 * slot,
                outliers=outliers[i][j], orientation=orientation,
                label=label, ax=staging, **style,
            ))
        commands.append(row)

    ax = ax if ax is not None else __get_or_create_ax()
    for requirement in staging.requirements.get_code().splitlines():
        if requirement not in ax.requirements.get_code().splitlines():
            ax.add_requirement(requirement)
    for row in commands:
        for command in row:
            ax.add(command)
    ticks = np.arange(1, n_experiments + 1)
    if orientation == "vertical":
        ax.set_xticks(ticks, experiment_labels)
    else:
        ax.set_yticks(ticks, experiment_labels)
    return commands


def surf(
    x, y, z, ax: Axis | None = None, label: str | None = None, **options
) -> Addplot:
    ax = ax if ax is not None else __get_or_create_ax()
    plot = create_surface_plot(x, y, z, label, **options)
    ax.add(plot)
    return plot


def contour(x, y, z, ax: Axis | None = None, **options) -> list[Contour]:
    from .util import get_extremes_safely

    ax = ax if ax is not None else __get_or_create_ax()
    contours, levels = create_contour(x, y, z, **options)
    for contour in contours:
        ax.add(contour)
    min, max = get_extremes_safely(levels)
    ax.set_option("point meta min", min)
    ax.set_option("point_meta_max", max)
    return contours


def contourf(x, y, z, ax: Axis | None = None, **options) -> list[ContourFilled]:
    from .util import get_extremes_safely

    ax = ax if ax is not None else __get_or_create_ax()
    contours, levels = create_contourf(x, y, z, **options)
    for contour in contours:
        ax.add(contour)
    min, max = get_extremes_safely(levels)
    ax.set_option("point meta min", min)
    ax.set_option("point_meta_max", max)
    ax.set_option("unbounded coords", "jump")
    return contours


def colorbar(ax: Axis | None = None):
    ax = ax if ax is not None else __get_or_create_ax()
    ax.set_option("colorbar", True)


def scatter(
    x,
    y=None,
    z=None,
    ax: Axis | None = None,
    label: str | tuple[str] | None = None,
    inline_label: bool = False,
    **options,
) -> list[Addplot]:
    """
    Create a scatter plot command.

    Parameters
    ----------
    x : array-like
        x-coordinates or data
    y : array-like, optional
        y-coordinates
    z : array-like, optional
        z-coordinates for 3D plots
    ax : Axis, optional
        Axis to add the plot to
    label : str | tuple[str], optional
        Label or tuple of labels for the plot
    inline_label : bool, optional
        Whether to place label inline with the plot, by default False
    **options
        Additional plotting options

    Returns
    -------
    list[Addplot]
        List of plot commands created
    """
    options["only marks"] = True
    return plot(x, y, z, ax, label, inline_label, **options)


def semilogy(ax: Axis | None = None):
    from .environments.axis import AxisMode

    ax = __get_or_create_ax() if ax is None else ax
    ax.set_xmode(AxisMode.linear.value)
    ax.set_ymode(AxisMode.log.value)


def semilogx(ax: Axis | None = None):
    from .environments.axis import AxisMode

    ax = __get_or_create_ax() if ax is None else ax
    ax.set_xmode(AxisMode.log.value)
    ax.set_ymode(AxisMode.linear.value)


def loglog(ax: Axis | None = None):
    from .environments.axis import AxisMode

    ax = __get_or_create_ax() if ax is None else ax
    ax.set_xmode(AxisMode.log.value)
    ax.set_ymode(AxisMode.log.value)


def preamble(fig: TikzPicture | None = None) -> TikzCode:
    fig = __get_or_create_fig() if fig is None else fig
    return fig.preamble
