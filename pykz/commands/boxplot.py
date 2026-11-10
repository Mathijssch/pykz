from .addplot import Addplot


class Boxplot(Addplot):
    """A prepared PGFPlots box plot with optional outlier coordinates."""

    def get_code(self) -> str:
        # The statistics handler interprets the second coordinate as the sample
        # value for either draw direction; the first coordinate is ignored.
        coordinates = "\n".join(f"(0, {value:.16g})" for value in self.data)
        legend = f"\\addlegendentry{{{self.label}}}" if self.label else ""
        return (
            f"\\addplot{self.options.format()} coordinates {{\n"
            f"{coordinates}\n}};\n{legend}\n"
        )
