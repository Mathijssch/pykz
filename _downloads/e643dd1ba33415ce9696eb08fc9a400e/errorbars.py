"""
Error bars: distances and endpoints
==================================
Show uncertainty using error distances or absolute interval endpoints.
"""

# %%
# To indicate errors on a plot you have several option. 
# You may either pass (1) a scalar error, which gets applied to every datapoint; or
# (2) a tuple / list of errors, one for each datapoint. 
# You can specify errors both for the x and the y component of the data.
#
# By default, subsequent data points are connected by a line. To suppress this line, 
# use the option ``only_marks``. Additional options present in the ``pgfplots`` errorbars 
# API can also be passed through keyword arguments.
import pykz

x = [1, 2, 3, 4]
y = [10, 15, 12, 18]
pykz.figure()
pykz.ax(xlabel="Experiment", ylabel="Measurement")
pykz.errorbar(
    x, y, xerr=0.1, yerr=[1, 2, 1.5, 2.5],
    color="cyan", mark="*", only_marks=True,
)
pykz.save("errorbars_symmetric.tex", standalone=True)
pykz.io.export_pdf_from_file("errorbars_symmetric.tex")

# %%
# To pass asymmetric errors, pass two rows: lower errors first, upper errors second.
# Alternatively, you may pass absolute bounds instead give the actual lower and upper ends.
# Here the two methods use different conventions on the same axis, with consistent styling.
pykz.figure()
pykz.ax(xlabel="Experiment", ylabel="Measurement", legend_pos="north west")
pykz.errorbar(
    x, y, yerr=([1, 2, 1, 2], [2, 1, 3, 1]),
    color="cyan", mark="*", label="Method A: distances",
)
pykz.errorbar(
    x, [8, 11, 10, 14], ybounds=([6, 10, 8, 12], [9, 13, 11, 17]),
    color="red", mark="square*", label="Method B: endpoints",
    error_style="thick",
    error_mark_options={"rotate": 90, "mark_size": "3pt"},
)
pykz.save("errorbars_comparison.tex", standalone=True)
pykz.io.export_pdf_from_file("errorbars_comparison.tex")

# %%
# Conventions may also differ between the x and y axes. Bounds are in original data units,
# and either endpoint can be a scalar shared by all points. Both axes below
# have asymmetric error bars.
# The returned Errorbar object also lets you customize styles after creation.
# These setters merge settings, so adding thick=True preserves the cyan color.
# set_mark_options affects the end caps rather than the data-point markers.
pykz.figure()
pykz.ax(xlabel="Input", ylabel="Measurement")
er = pykz.errorbar(
    x, y,
    xerr=([0.1, 0.2, 0.1, 0.3], [0.3, 0.1, 0.2, 0.1]),
    ybounds=(5, [12, 16, 15, 20]),
    color="cyan", mark="*", only_marks=True,
    error_style={"color": "cyan"},
)
er.set_error_style(thick=True)
er.set_mark_options(rotate=90, mark_size="3pt")
pykz.save("errorbars_mixed.tex", standalone=True)
pykz.io.export_pdf_from_file("errorbars_mixed.tex")
