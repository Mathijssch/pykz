import numpy as np
import pytest

import pykz
from pykz.plot import create_errorbar


def test_distances_and_bounds_are_equivalent_and_inputs_unchanged():
    x = np.array([1., 2., 3.])
    y = np.array([10., 15., 12.])
    errors = np.array([[2., 3., 1.], [3., 2., 4.]])
    bounds = np.array([[8., 12., 11.], [13., 17., 16.]])
    originals = [a.copy() for a in (x, y, errors, bounds)]
    distances = create_errorbar(x, y, xerr=0.5, yerr=errors)
    endpoints = create_errorbar(x, y, xbounds=(x - .5, x + .5), ybounds=bounds)
    assert distances.get_code() == endpoints.get_code()
    np.testing.assert_array_equal(distances.data[:, 2:4], np.full((3, 2), .5))
    np.testing.assert_array_equal(distances.data[:, 4:6], errors.T)
    code = distances.get_code()
    for key, index in [("x error minus", 2), ("x error plus", 3),
                       ("y error minus", 4), ("y error plus", 5)]:
        assert f"{key} index={{{index}}}" in code
    for value, original in zip((x, y, errors, bounds), originals):
        np.testing.assert_array_equal(value, original)


def test_scalar_bounds_and_symmetric_errors():
    command = create_errorbar([1, 2], [10, 15], xerr=[.1, .2], ybounds=(5, [12, 15]))
    np.testing.assert_allclose(command.data, [
        [1, 10, .1, .1, 5, 2], [2, 15, .2, .2, 10, 0],
    ])


def test_explicit_axis_labels_and_styles():
    fig = pykz.figure()
    axis = pykz.ax()
    pykz.figure()
    command = pykz.errorbar([1, 2], [3, 4], yerr=.2, ax=axis, label="Data",
                             color="cyan", only_marks=True,
                             **{"error bars/y dir": "plus"})
    assert isinstance(command, pykz.Errorbar)
    code = pykz.dumps(fig)
    assert r"\addlegendentry{Data}" in code
    assert "error bars/y dir={plus}" in code
    assert "only marks" in code
    assert "error bars/x explicit" not in code
    assert r"\addplot" not in pykz.dumps()


def test_implicit_indices_no_errors_and_inline_label():
    pykz.figure()
    command = pykz.errorbar([3, 4], label="Data", inline_label=True)
    np.testing.assert_array_equal(command.data, [[0, 3], [1, 4]])
    code = command.get_code()
    assert "error bars/" not in code
    assert "node" in code and "{Data}" in code
    assert "forget plot" in code
    assert r"\addlegendentry" not in code


@pytest.mark.parametrize("kwargs", [
    {"yerr": -1}, {"yerr": np.nan}, {"yerr": [1]},
    {"yerr": [[1, 2, 3], [1, 2, 3]]},
    {"yerr": 1, "ybounds": (0, 5)},
    {"xerr": 1, "xbounds": (0, 5)},
    {"ybounds": (4, 5)}, {"ybounds": (0, 2)},
    {"ybounds": (0, np.inf)}, {"ybounds": ([0], [5])},
    {"ybounds": (0, 4, 5)}, {"ybounds": 5},
])
def test_invalid_errors_do_not_modify_axis(kwargs):
    pykz.figure()
    pykz.ax(title="Existing")
    before = pykz.dumps()
    with pytest.raises(ValueError):
        pykz.errorbar([1, 2], [3, 4], **kwargs)
    assert pykz.dumps() == before


@pytest.mark.parametrize("x,y", [([], []), ([1], [2, 3]), ([[1, 2]], [3, 4]), (1, None)])
def test_invalid_coordinates_do_not_create_axis(x, y):
    pykz.figure()
    with pytest.raises(ValueError):
        pykz.errorbar(x, y)
    assert pykz.gca() is None


def test_mutable_styles_merge_and_update_figure():
    pykz.figure()
    style = {"color": "red"}
    caps = {"rotate": 90, "mark_size": "2pt"}
    er = pykz.errorbar([1, 2], [3, 4], yerr=.2, mark="square*",
                       error_style=style, error_mark_options=caps)
    before = pykz.dumps()
    assert er.set_error_style(thick=True) is er
    assert er.set_mark_options(mark_size="3pt") is er
    assert er.set_error_style(color="cyan") is er
    code = pykz.dumps()
    assert code != before
    assert "error bars/error bar style={color={cyan},\nthick}" in code
    assert "error bars/error mark options={rotate={90},\nmark size={3pt}}" in code
    assert "mark={square*}" in code
    assert style == {"color": "red"}
    assert caps == {"rotate": 90, "mark_size": "2pt"}
    assert code.count("error bars/error bar style=") == 1


def test_raw_styles_preserved_and_updates_take_precedence():
    er = create_errorbar([1], [2], yerr=.1, error_style="thick,color=red",
                         error_mark_options="rotate=90,mark size=2pt")
    er.set_error_style(color="cyan").set_mark_options(mark_size="3pt")
    er.set_error_style(line_width="2pt")
    code = er.get_code()
    assert "thick,color=red,color={cyan},line width={2pt}" in code
    assert "rotate=90,mark size=2pt,mark size={3pt}" in code


def test_named_styles_override_qualified_options():
    er = create_errorbar([1], [2], yerr=.1,
                         error_style={}, error_mark_options={"rotate": 90},
                         **{"error bars/error bar style": "thin",
                            "error bars/error mark options": "mark size=9pt"})
    assert "thin" not in er.get_code()
    assert "9pt" not in er.get_code()
    er.set_error_style(thick=True)
    assert "error bars/error bar style={thick}" in er.get_code()


def test_setters_work_with_qualified_options_and_defaults():
    er = create_errorbar([1], [2], **{"error bars/error bar style": "thick"})
    er.set_error_style(color="red").set_mark_options(rotate=90)
    assert "thick,color={red}" in er.get_code()
    assert "error bars/error mark options={rotate={90}}" in er.get_code()


@pytest.mark.parametrize("kwargs", [{"error_style": 1}, {"error_mark_options": []}])
def test_invalid_style_does_not_create_axis(kwargs):
    pykz.figure()
    with pytest.raises(TypeError):
        pykz.errorbar([1], [2], **kwargs)
    assert pykz.gca() is None
