# Changelog

## 0.3.0

### Added

- Bar plots and histograms through `pykz.bar()` and `pykz.hist()`.
- Box plots from precomputed whiskers, quartiles, and medians, with optional
  outliers and horizontal orientation.
- `pykz.grouped_boxplot()` for comparing methods across experiments, with
  automatic positions, widths, ticks, and legend entries.
- `pykz.errorbar()` with symmetric or asymmetric error distances (`xerr`,
  `yerr`) and absolute endpoints (`xbounds`, `ybounds`).
- An `Errorbar` object with `set_error_style()` and `set_mark_options()` methods
  for post-creation customization.
- Documentation gallery examples for bars, histograms, box plots, grouped
  comparisons, and error bars.
- Configurable LaTeX compilation commands and arguments for PDF and PNG exports,
  including support for LuaLaTeX and XeLaTeX via `cmd` and `cmd_args`.

### Fixed

- Isolate the gallery's active figure and axis between examples, and collect
  only PDFs created or updated by the current example. Leftover PDFs no longer
  appear in unrelated gallery pages.
- Update the PyPI publishing action to `pypa/gh-action-pypi-publish@v1.14.3`.

### Compatibility

- Package metadata now requires Python 3.10 or newer.
- `pykz.errorbar()` returns a single `Errorbar` object. Users of the unreleased
  development implementation should replace `er, = pykz.errorbar(...)` with
  `er = pykz.errorbar(...)`. The return types of `plot()` and `scatter()` are
  unchanged for now. Bigger API changes are planned, including some breaking changes, but they will be postponed to a major version update.

