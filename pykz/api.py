"""Public API"""

from __future__ import annotations

from .environments.axis import Axis
from .environments.tikzpicture import TikzPicture
from .commands.addplot import Addplot
from .commands.fillbetween import FillBetween
from .commands.node import Node
from .commands.draw import Draw
from .commands.circle import Circle
from .plot import create_plot
import numpy as np
from typing import Optional, Union


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


def dumps(fig: TikzPicture = None) -> str:
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


def preview(fig: TikzPicture = None):
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


def save(filename: str, fig: TikzPicture = None, standalone: bool = False):
    """
    Save the generated Tikz code to a file.

    Parameters
    ----------
    filename : str
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


def xticks(ticks: np.ndarray, labels: list[str] = None, ax: Axis = None):
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


def yticks(ticks: np.ndarray, labels: list[str] = None, ax: Axis = None):
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


def zticks(ticks: np.ndarray, labels: list[str] = None, ax: Axis = None):
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


def define_style(name: str, fig: TikzPicture = None, **options):
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


def axhline(y: float, ax: Axis = None, **options) -> list[Addplot]:
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
    return plot(y, ax, **options)


def scale(scale: float, fig: TikzPicture = None):
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


def point(coordinates: np.ndarray = None,
          label: str = "",
          name: str = None,
          axis_coords: bool = None,
          label_loc: str = "above",
          size: int | str = "1pt",
          axis: Axis = None,
          fig: TikzPicture = None,
          **options) -> Node:
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


def node(coordinates: np.ndarray = None,
         label: str = None,
         name: str = None,
         axis_coords: bool = None,
         label_loc: str = None,
         axis: Axis = None,
         fig: TikzPicture = None,
         **options) -> Node:
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


def fill_between(x: np.ndarray, y1: np.ndarray, y2: np.ndarray, *,
                 draw_options=None, fill_options=None) -> FillBetween:
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


def axvline(x: float, ax: Axis = None, **options) -> list[Addplot]:
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
    """    # TODO: Think of ways to represent this allow axes dimensions to be updated afterwards.
    ax = ax if ax is not None else __get_or_create_ax()
    ymin, ymax = ax.get_ylims()
    xes = np.array((x, x))
    ys = np.array((ymin, ymax))
    return plot(xes, ys, ax=ax, **options)


Point = Union[np.ndarray, str, Node]


def __create_draw(connector_type: str, points: list[Point], **options) -> Draw:
    from pykz.commands import Connector
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


def arrow(points: list[Point], forward: bool = True, backward: bool = False,
          arrowhead: str = None, **options) -> Draw:
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


def plot(x, y=None, z=None, ax: Axis = None, label: str | tuple[str] = None,
         inline_label: bool = False,
         **options) -> list[Addplot]:
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


def scatter(x, y=None, z=None, ax: Axis = None, label: str | tuple[str] = None,
            inline_label: bool = False,
            **options) -> list[Addplot]:
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
