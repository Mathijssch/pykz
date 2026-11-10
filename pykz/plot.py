from __future__ import annotations

import numpy as np
from .commands.addplot import Addplot, Addplot3d
from .commands.errorbar import Errorbar
from .constants import MAX_NUMBER


def remove_huge_nbs(arr):
    mask = np.abs(arr) > MAX_NUMBER
    arr[mask] = np.sign(arr[mask]) * np.inf
    return arr


def create_errorbar(
    x, y=None, *, xerr=None, yerr=None, xbounds=None, ybounds=None,
    label=None, inline_label=False, error_style=None, error_mark_options=None,
    **options,
) -> Errorbar:
    """Normalize a single series and its errors into an explicit PGFPlots table."""
    from .options import Options

    if y is None:
        y = np.array(x, dtype=float, copy=True)
        x = np.arange(y.size, dtype=float)
    else:
        x = np.array(x, dtype=float, copy=True)
        y = np.array(y, dtype=float, copy=True)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size or not x.size:
        raise ValueError("x and y must be nonempty one-dimensional sequences of equal length.")

    def normalize(coordinates, errors, bounds, name):
        if errors is not None and bounds is not None:
            raise ValueError(f"{name}err and {name}bounds are mutually exclusive.")
        if errors is None and bounds is None:
            return None
        if bounds is not None:
            try:
                lower, upper = bounds
            except (TypeError, ValueError):
                raise ValueError(f"{name}bounds must contain lower and upper endpoints.") from None

            def endpoint(value):
                value = np.asarray(value, dtype=float)
                if value.ndim == 0:
                    return np.full(coordinates.size, value)
                if value.shape != coordinates.shape:
                    raise ValueError(f"{name}bounds endpoints must be scalars or length N.")
                return value

            lower, upper = endpoint(lower), endpoint(upper)
            if not (np.all(np.isfinite(lower)) and np.all(np.isfinite(upper))
                    and np.all(np.isfinite(coordinates))):
                raise ValueError(f"{name}bounds and their coordinates must be finite.")
            with np.errstate(over="ignore", invalid="ignore"):
                result = np.array([coordinates - lower, upper - coordinates])
        else:
            errors = np.asarray(errors, dtype=float)
            if errors.ndim == 0:
                result = np.full((2, coordinates.size), errors)
            elif errors.shape == coordinates.shape:
                result = np.stack([errors, errors])
            elif errors.shape == (2, coordinates.size):
                result = errors
            else:
                raise ValueError(f"{name}err must be a scalar, length N, or shape (2, N).")
        if not np.all(np.isfinite(result)) or np.any(result < 0):
            raise ValueError(
                f"{name} errors must be finite and nonnegative; bounds must enclose the coordinates."
            )
        return result

    columns = [x, y]
    table_options = {"x index": 0, "y index": 1}
    opts = Options(**options)
    for direction, coordinates, errors, bounds in (
        ("x", x, xerr, xbounds), ("y", y, yerr, ybounds),
    ):
        normalized = normalize(coordinates, errors, bounds, direction)
        if normalized is None:
            continue
        table_options[f"{direction} error minus index"] = len(columns)
        table_options[f"{direction} error plus index"] = len(columns) + 1
        columns.extend(normalized)
        opts.set_option(f"error bars/{direction} explicit", True)
        if f"error bars/{direction} dir" not in opts:
            opts.set_option(f"error bars/{direction} dir", "both")
    if (label is None or inline_label) and "forget plot" not in opts:
        opts.set_option("forget plot", True)
    command = Errorbar(
        remove_huge_nbs(np.column_stack(columns)), label,
        inline_label=inline_label, error_style=error_style,
        error_mark_options=error_mark_options, **opts,
    )
    for key, value in table_options.items():
        command.set_table_option(key, value)
    return command


def create_surface_plot(
    x: np.ndarray, y: np.ndarray, z: np.ndarray, label: str | None = None, **options
) -> Addplot3d:
    shape = x.shape
    assert len(shape) == 2, (
        f"Expected a 2-dimensional array for a surface plot. Got shape: {shape}"
    )

    if y is None:  # Plot index vs. x
        x_range = np.arange(shape[0])
        y_range = np.arange(shape[1])
        z = x
        x, y = np.meshgrid(x_range, y_range)

    x = remove_huge_nbs(np.array(x))
    y = remove_huge_nbs(np.array(y))
    z = remove_huge_nbs(np.array(z))

    rows = []

    for x_r, y_r, z_r in zip(x, y, z):
        rows.append(
            "\\\\\n".join(
                [f"{x:16f} {y:16f} {z:16f}" for x, y, z in zip(x_r, y_r, z_r)]
            )
        )

    formatted_table = "\\\\\n\\\\\n".join(rows) + r"\\"

    def forget_plot(label):
        if (label is None) and ("forget_plot" not in options):
            return {"forget plot": True}
        return {}

    options["surf"] = True

    plot3d = Addplot3d(formatted_table, label, **forget_plot(label), **options)
    # del plot3d._table_opts["row sep"]
    return plot3d


def create_plot(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    label: str | None = None,
    inline_label: bool = False,
    **options,
) -> list[Addplot]:
    plot3d = False

    if y is None:  # Plot index vs. x
        if np.ndim(x) == 0:  # Constant
            datasets = [np.array(x)]
        else:
            datasets = (
                np.hstack((np.arange(len(row))[:, np.newaxis], row[:, np.newaxis]))
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
                np.hstack(
                    (x_row[:, np.newaxis], y_row[:, np.newaxis], z_row[:, np.newaxis])
                )
                for x_row, y_row, z_row in zip(
                    np.atleast_2d(x), np.atleast_2d(y), np.atleast_2d(z)
                )
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
        if (label is None or inline_label) and ("forget_plot" not in options):
            return {"forget plot": True}
        return {}

    # Set large numbers to infinity because pgfplots doesn't handle them.
    datasets = (remove_huge_nbs(a) for a in datasets)

    constructor = Addplot3d if plot3d else Addplot

    return [
        constructor(
            dataset, lab, inline_label=inline_label, **forget_plot(lab), **options
        )
        for lab, dataset in zip(iter_label(), datasets)
    ]
