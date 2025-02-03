from __future__ import annotations

from ..command import Command
from ..style import Style
from collections import OrderedDict


class Tikzset(Command):

    def __init__(self,
                 styles: list[Style] = None,
                 ):
        self._style_map = OrderedDict()
        if styles:
            for style in styles:
                self._style_map[style.name] = style

        super().__init__("tikzset")
        self._endline = False

    def add_argument(self, argument: Style):
        raise NotImplementedError("To add a new style to tikzset, use the ``set_style`` method.")

    @property
    def arguments(self) -> list[Style]:
        return list(self._style_map.values())

    def set_style(self, name: str, **options):
        if name in self._style_map:
            style: Style = self._style_map[name]
            return style.set_options(**options)
        new_style = Style(name, **options)
        self._style_map[name] = new_style

    def get_code(self) -> str:
        if not self._style_map:
            return ""
        return super().get_code()

    def remove_style(self, name: str):
        try:
            self._style_map.pop(name)
        except KeyError:
            raise UserWarning("Tried to remove undefined style.")
