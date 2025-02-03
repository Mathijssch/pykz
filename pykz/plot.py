from __future__ import annotations

import numpy as np
from .commands.addplot import Addplot, Addplot3d
from .constants import MAX_NUMBER


def remove_huge_nbs(arr):
    mask = np.abs(arr) > MAX_NUMBER
    arr[mask] = np.sign(arr[mask]) * np.inf
    return arr


def create_plot(x: np.ndarray, y: np.ndarray, z: np.ndarray, label: str | None = None, inline_label: bool = False, **options) -> list[Addplot]:
    plot3d = False

    if y is None:  # Plot index vs. x
        if np.ndim(x) == 0:  # Constant
            datasets = [np.array(x)]
        else:
            datasets = (
                np.hstack((np.arange(len(row))[:, np.newaxis],
                           row[:, np.newaxis]))
                for row in np.atleast_2d(x)
            )
    else:
        if z is None:
            datasets = (
                np.hstack((x_row[:, np.newaxis], y_row[:, np.newaxis]))
                for x_row, y_row in zip(np.atleast_2d(x), np.atleast_2d(y))
            )
        else:
            plot3d = True
            datasets = (
                np.hstack((x_row[:, np.newaxis], y_row[:, np.newaxis], z_row[:, np.newaxis]))
                for x_row, y_row, z_row in zip(np.atleast_2d(x), np.atleast_2d(y), np.atleast_2d(z))
            )

    def iter_label():
        if label is None:
            yield None
        elif isinstance(label, str):
            while True:
                yield label
        else:
            for lab in label:
                yield lab
            yield None

    def forget_plot(label):
        if (label is None or inline_label) \
                and ("forget_plot" not in options) \
                and ("forget plot" not in options):
            return {"forget plot": True}
        return {}

    # Set large numbers to infinity because pgfplots doesn't handle them.
    datasets = (remove_huge_nbs(a) for a in datasets)

    constructor = Addplot3d if plot3d else Addplot

    return [constructor(dataset, lab, inline_label=inline_label, **forget_plot(lab), **options) for lab, dataset in zip(iter_label(), datasets)]
