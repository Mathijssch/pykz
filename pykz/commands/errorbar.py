"""PGFPlots error-bar commands with convenient style updates."""

from collections.abc import Mapping

from .addplot import Addplot
from ..options import Options


class Errorbar(Addplot):
    """A single series with independently configurable error lines and end caps.

    Returned by :func:`pykz.errorbar`. General plot options and label methods
    inherited from Addplot remain available.
    """

    def __init__(
        self, data, label=None, inline_label=False, *,
        error_style=None, error_mark_options=None, **options,
    ):
        super().__init__(data, label, inline_label, **options)
        for key, value in (
            ("error bars/error bar style", error_style),
            ("error bars/error mark options", error_mark_options),
        ):
            value = self.options.get(key) if value is None else value
            if value is not None:
                self.set_option(key, self._style(value))

    @staticmethod
    def _style(value):
        if isinstance(value, Mapping):
            return Options(**value)
        if isinstance(value, str):
            return value
        raise TypeError("Error-bar styles must be mappings or PGFPlots strings.")

    def _update_style(self, key, options):
        current = self._style(self.options.get(key, Options()))
        updates = Options(**options)
        if isinstance(current, Options):
            current.set_options(**updates)
        else:
            # Preserve arbitrary TeX without attempting to parse its commas or
            # braces. PGFPlots applies the appended settings last.
            current = ",".join(filter(None, (current, updates.format(False))))
        self.set_option(key, current)
        return self

    def set_error_style(self, **options):
        """Merge error-line styling and return self for chaining.

        For example, ``er.set_error_style(thick=True, color="red")``.
        Existing settings are preserved; matching keys use the latest value.
        Raw PGFPlots strings are preserved with new options appended.
        """
        return self._update_style("error bars/error bar style", options)

    def set_mark_options(self, **options):
        """Merge error-bar end-cap options and return self for chaining.

        For example, ``er.set_mark_options(rotate=90, mark_size="3pt")``.
        These options affect the end caps, not the data-point markers.
        Underscores in option names are converted to spaces.
        """
        return self._update_style("error bars/error mark options", options)
