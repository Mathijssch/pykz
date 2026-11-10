import numpy as np
import pytest

import pykz


def test_grouped_boxes_on_explicit_axis():
    fig = pykz.figure()
    axis = pykz.ax()
    pykz.figure()  # The target need not belong to the current figure.
    first = pykz.boxplot(1, 2, 3, 4, 5, position=0.8, width=0.3,
                         outliers=[0, 7], label="Method A", ax=axis)
    second = pykz.boxplot(2, 2, 2, 2, 2, position=1.2, ax=axis)
    code = pykz.dumps(fig)
    assert code.count(r"\usepgfplotslibrary{statistics}") == 1
    assert code.count(r"\addplot[") == 2
    assert code.count(r"\addlegendentry{Method A}") == 1
    assert "draw position={0.8}" in code
    assert "boxplot/box extend={0.3}" in code
    assert "(0, 0)" in code and "(0, 7)" in code
    assert "forget plot" not in first.options
    assert second.options["forget plot"]
    assert "statistics" not in pykz.dumps()


def test_horizontal_and_implicit_axis():
    pykz.figure()
    box = pykz.boxplot(1, 2, 3, 4, 5, orientation="horizontal", fill="blue!20")
    assert box.options["boxplot/draw direction"] == "x"
    assert box.options["fill"] == "blue!20"
    assert "coordinates {\n\n}" in box.get_code()
    assert "statistics" in pykz.dumps()


@pytest.mark.parametrize("kwargs", [
    {"width": 0}, {"width": -1}, {"width": np.inf},
    {"position": np.nan}, {"orientation": "diagonal"},
    {"outliers": [np.nan]}, {"outliers": [[1, 2]]},
])
def test_invalid_options(kwargs):
    with pytest.raises(ValueError):
        pykz.boxplot(1, 2, 3, 4, 5, **kwargs)


@pytest.mark.parametrize("statistics", [(2, 1, 3, 4, 5), (1, 2, np.inf, 4, 5)])
def test_invalid_statistics(statistics):
    with pytest.raises(ValueError):
        pykz.boxplot(*statistics)
