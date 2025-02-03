from __future__ import annotations

from typing import Union
from .formatting import format_options


class Tex:

    def __init__(self, code: str):
        self.code = code

    def __str__(self) -> str:
        return self.get_code()

    def get_code(self) -> str:
        return self.code


class TikzCode:
    """Low-level representation of tikz code.
    The tikz code is represented as a list of lines.
    The methods of this function can be used to easily add new
    lines to the tikz code.
    """

    def __str__(self) -> str:
        return self.get_code()

    def __repr__(self) -> str:
        return f"{self.__class__}\n{self.get_code()}"

    def __init__(self):
        self.lines = []

    def __cmd(self, cmd: str) -> "TikzCode":
        self.add_line(Tex(cmd))
        return self

    def colorlet(self, colorname: str, colordef: str) -> "TikzCode":
        """Define a new color using the ``\\colorlet`` command of xcolor."""
        return self.__cmd(f"\\colorlet{{{colorname}}}{{{colordef}}}")

    def definecolor(self, colorname: str, kind: str, definition: str) -> "TikzCode":
        """Define a new color using the ``\\definecolor`` command."""
        return self.__cmd(f"\\definecolor{{{colorname}}}{{{kind}}}{{{definition}}}")

    def usepackage(self, package: str, **options) -> "TikzCode":
        return self.__cmd(f"\\usepackage{format_options(**options)}{{{package}}}")

    def newcommand(self, command: str, definition, n_args: int = 0) -> "TikzCode":
        argcnt = f"[{n_args}]" if n_args > 0 else ""
        return self.__cmd(f"\\newcommand{{\\{command}}}{argcnt}{{{definition}}}")

    def node(self,
             label_text: str, name: str = "", location: Union[tuple, str] = "",
             **options) -> "TikzCode":
        location_str = f"at {location}" if location else ""
        return self.__cmd(f"\\node{format_options(**options)} ({name}) {location_str} {{{label_text}}};")

    def coordinate(self, name: str = "", location: Union[tuple, str] = "", **options) -> "TikzCode":
        location_str = f"at {location}" if location else ""
        return self.__cmd(f"\\coordinate{format_options(**options)} ({name}) {location_str};")

    def draw(self, *coordinates, **options) -> "TikzCode":
        return self.__cmd(f"\\draw{format_options(**options)} {'--'.join(coordinates)};")

    def add_line(self, line: Tex | str) -> "TikzCode":
        if isinstance(line, str):
            line = Tex(line)
        self.lines.append(line)

    def get_code(self) -> str:
        return "\n".join(line.get_code() for line in self.lines) + "\n"
