"""
Minimal working example
=========================
Minimal working example of `pykz`, plotting a simple sine function.
"""

# %%
import numpy as np
import pykz

x = np.linspace(0, 10, 100)
y = np.sin(x)

pykz.plot(x, y)

# Export your tex code as a standalone file
pykz.save("basic_inline.tex", standalone=True)
# You could also directly build the pdf
pykz.io.export_pdf_from_file("basic_inline.tex")

# %%
# Alternatively, output it to png
#
# .. code-block:: python
#
#   pykz.io.export_png_from_file("basic_inline.tex")
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
