"""
A Matplotlib-like interface for generating Tikz and Pgfplots figures
"""

__version__ = "0.1.4"

from .api import (
    gcf,
    gca,
    figure,
    ax,
    dumps,
    preview,
    save,
    xlabel,
    xticks,
    yticks,
    zticks,
    define_style,
    ylabel,
    zlabel,
    xlim,
    ylim,
    axhline,
    scale,
    node,
    fill_between,
    axvline,
    Point,
    rectangle,
    circle,
    line,
    arrow,
    plot,
    scatter,
    point,
)
from .environments.axis import Grid, Axis, AxisMode, AxisDir, View
from . import io
