from __future__ import annotations

from .. import formatting
from ..tikzcode import TikzCode
from ..commands.tikzset import Tikzset
# from ..command import Command
from .. import environment as env
from . import axis as ax


class TikzPicture(env.Environment):

    def __init__(self, standalone: bool = True, **options):
        super().__init__("tikzpicture", **options)
        self.standalone = standalone
        self.preamble = TikzCode()
        self._styles = Tikzset()
        # self._styles: OrderedDict[str, Options] = OrderedDict()

    def add_preamble_line(self, line: str):
        self.preamble.add_line(line)

    def remove_style(self, name: str):
        self._styles.remove_style(name)

    def set_style(self, name: str, **options):
        self._styles.set_style(name, **options)

    def define_style(self, name: str, **options):
        """Define (or update if it already exists) a style with the given name."""
        DeprecationWarning("`define_style` is deprecated. Use `set_style` instead.")
        self.set_style(name, **options)

    def add_axis(self, axis: ax.Axis | None = None):
        axis = ax.Axis() if axis is None else axis
        self.add(axis)
        self.preamble.usepackage("pgfplots")
        # self.preamble.add_line(Command("pgfplotsset", "compat=1.18"))

    def generate_preamble(self) -> str:
        preamble = self.preamble.get_code()
        for content in self.content.lines:
            if isinstance(content, env.Environment):
                preamble += (content.requirements.get_code())
        return preamble

    def format_styles(self) -> str:
        if not self._styles:
            return ""
        return self._styles.get_code() + "\n"

    def get_code(self) -> str:
        preamble = ""
        if self.standalone:
            preamble += "\\documentclass[tikz, margin=5]{standalone}\n"
            preamble += self.generate_preamble()
        else:
            preamble += "% Add the following lines in the preamble: \n"
            for line in self.generate_preamble().splitlines():
                preamble += f"%{line}\n"

        preamble += self.format_styles()
        content = self.content.get_code()
        content = formatting.wrap_env("tikzpicture", content, **self.options)
        if self.standalone:
            content = formatting.wrap_env("document", content)

        return preamble + content

    def export(self, filename: str):
        # Create the file directory if it doesn't exist already.
        import os
        parent = os.path.dirname(filename)
        if parent:
            os.makedirs(os.path.dirname(filename), exist_ok=True)

        if not filename.endswith(".tex") and \
           not filename.endswith(".tikz"):
            filename = filename + ".tex"

        with open(filename, "w") as f:
            f.write(self.get_code())

    def preview(self):
        from ..io import preview_latex_doc
        is_standalone = self.standalone
        self.standalone = True
        prev = preview_latex_doc(self.get_code())
        self.standalone = is_standalone  # Reset to initial state
        return prev
