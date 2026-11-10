import numpy as np
import pytest

import pykz


@pytest.mark.parametrize("n_methods", [1, 2, 3, 8])
def test_layout(n_methods):
    pykz.figure()
    summaries = np.tile([1, 2, 3, 4, 5], (3, n_methods, 1))
    boxes = pykz.grouped_boxplot(summaries)
    assert len(boxes) == 3
    for center, row in enumerate(boxes, start=1):
        assert len(row) == n_methods
        positions = [box.options["boxplot prepared"]["draw position"] for box in row]
        widths = [box.options["boxplot/box extend"] for box in row]
        assert np.mean(positions) == pytest.approx(center)
        assert positions[0] - widths[0] / 2 > center - 0.4
        assert positions[-1] + widths[-1] / 2 < center + 0.4
        assert np.all(np.diff(positions) > widths[0])


def test_horizontal_labels_styles_and_outliers():
    fig = pykz.figure()
    axis = pykz.ax()
    pykz.figure()
    boxes = pykz.grouped_boxplot(
        np.tile([1, 2, 3, 4, 5], (2, 2, 1)), ax=axis,
        experiment_labels=["A", "B"], method_labels=["First", "Second"],
        method_options=[{"fill": "cyan"}, {"fill": "red"}],
        outliers=[[[0, 8], None], [[], [9]]], orientation="horizontal",
        group_width=0.6, fill="black", draw="black",
    )
    code = pykz.dumps(fig)
    assert code.count(r"\addlegendentry") == 2
    assert "A" in axis.options["yticklabels"]
    assert "B" in axis.options["yticklabels"]
    assert "xticklabels" not in axis.options
    assert "(0, 9)" in code
    assert "statistics" not in pykz.dumps()
    for row in boxes:
        assert [box.options["fill"] for box in row] == ["cyan", "red"]
        for box in row:
            assert box.options["boxplot/draw direction"] == "x"
            assert box.options["boxplot/box extend"] == pytest.approx(0.24)
            assert box.options["draw"] == "black"
    assert boxes[1][0].options["forget plot"]


@pytest.mark.parametrize("kwargs", [
    {"experiment_labels": ["one"]}, {"method_labels": "ab"},
    {"method_options": [{}]}, {"outliers": [[[], []]]},
    {"outliers": [[[], []], [[], [np.inf]]]},
    {"group_width": 0}, {"group_width": 1.1},
    {"orientation": "diagonal"},
])
def test_invalid_options_leave_axis_untouched(kwargs):
    pykz.figure()
    pykz.ax(title="Existing axis")
    before = pykz.dumps()
    with pytest.raises(ValueError):
        pykz.grouped_boxplot(np.tile([1, 2, 3, 4, 5], (2, 2, 1)), **kwargs)
    assert pykz.dumps() == before


@pytest.mark.parametrize("summaries", [
    [], [[]], [[[1, 2, 3, 4]]],
    [[[1, 2, 3, 4, 5]], [[1, 2, 3, 4, np.nan]]],
    [[[1, 2, 3, 4, 5]], [[1, 3, 2, 4, 5]]],
])
def test_invalid_summaries_leave_workspace_untouched(summaries):
    pykz.figure()
    before = pykz.dumps()
    with pytest.raises(ValueError):
        pykz.grouped_boxplot(summaries)
    assert pykz.dumps() == before
    assert pykz.gca() is None
