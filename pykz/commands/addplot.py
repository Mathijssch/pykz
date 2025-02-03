from __future__ import annotations

from ..command import Command
from ..options import Options
from ..formatting import format_plot_command
import numpy as np


class __AddplotBase(Command):

    def __init__(self, data: np.ndarray,
                 plot3d: bool,
                 label: str,
                 inline_label: bool,
                 **options,
                 ):

        self.data = data
        self.label = label
        self._plot3d = plot3d
        self._inline_label = inline_label
        self._label_opts = Options(
            pos=0.7, above=True
        )
        super().__init__("addplot", **options)

    def customize_label(self, **options):
        """Customize the options of the inline label"""
        self._label_opts.set_options(**options)

    def get_code(self) -> str:
        return format_plot_command(self.data,
                                   raw_options=self.options.format(),
                                   plot3d=self._plot3d,
                                   label=self.label,
                                   inline_label=self._inline_label,
                                   labelopts=self._label_opts.format(),
                                   plotplus=False
                                   )


class Addplot(__AddplotBase):

    def __init__(self, data: np.ndarray,
                 label: str | None = None,
                 inline_label: bool = False,
                 **options,
                 ):
        super().__init__(data, False, label, inline_label, **options)


class Addplot3d(__AddplotBase):

    def __init__(self, data: np.ndarray,
                 label: str | None = None,
                 inline_label: bool = False,
                 **options,
                 ):
        super().__init__(data, True, label, inline_label, **options)
