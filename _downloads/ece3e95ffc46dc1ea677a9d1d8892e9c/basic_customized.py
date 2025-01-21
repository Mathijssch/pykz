"""
Basic customization
=====================

You can use keyword arguments to add options to your plots.
These options generate ``pgfkeys`` options in the final output.
Therefore, any string that can be interpreted by ``pdflatex`` is a
valid value.
"""

import numpy as np
import pykz
pykz.figure()

x = np.linspace(0, 10, 100)
y = np.sin(x)
y2 = np.cos(x)

pykz.plot(x, y, color="black", label="sine function")
pykz.plot(x, y2, color="blue", label="cosine function")

# Export your tex code as a standalone file
pykz.save("basic_customized.tex", standalone=True)
# You could also directly build the pdf
pykz.io.export_pdf_from_file("basic_customized.tex")

# %%
# Alternatively, output it to png
#
# .. code-block:: python
#
#   pykz.io.export_png_from_file("basic_customized.tex")
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
