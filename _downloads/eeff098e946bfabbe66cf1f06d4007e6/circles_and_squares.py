"""
Directly using Tikz
=====================

Directly use Tikz functionality, without pgfplots.
"""

import pykz
pykz.figure()

rect = pykz.rectangle((-1, -1), (1, 1))
circle = pykz.circle((2, 0), (1), fill="red")
rect2 = pykz.rectangle((1, 1), (2, 3), fill="cyan")

# Dump the generated tikz code to the stdout.
print(pykz.dumps())

# Export your tex code as a standalone file
pykz.save("circles_and_squares.tex", standalone=True)
# You could also directly build the pdf
pykz.io.export_pdf_from_file("circles_and_squares.tex")

# %%
# Alternatively, output it to png
#
# .. code-block:: python
#
#   pykz.io.export_png_from_file("circles_and_squares.tex")
#
# Or, save the Tikz code to a temporary file, compile it, and open the pdf in the default viewer.
# This would be the equivalent to ``plt.show()``
#
# .. code-block:: python
#
#   pykz.preview()
#
#
#
