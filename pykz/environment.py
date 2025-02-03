from __future__ import annotations

from dataclasses import dataclass
from .tikzcode import TikzCode, Tex
from .options import OptionsMixin
from typing import Union
from .formatting import wrap_env


@dataclass
class Environment(Tex, OptionsMixin):
    """Representation of a LaTeX environment."""

    def __init__(self, name: str, **options):
        self.name = name
        self.init_options(**options)
        self.content = TikzCode()
        self.requirements = TikzCode()  # Tikz code that should be added to the preamble

    def add(self, content: Union[Tex, str]):
        self.content.add_line(content)

    def get_code(self) -> str:
        return wrap_env(self.name, self.content.get_code(), **self.options)

    def add_requirement(self, req: str | Tex):
        self.requirements.add_line(req)

    def requires_package(self, package_name: str, **options):
        self.requirements.usepackage(package_name, **options)
