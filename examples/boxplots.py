"""
Box plots and grouped comparisons
=================================
Compare experiments using manually supplied summary statistics.
"""

# %%
# Supply the two whisker ends, two box edges, and median directly. No raw
# samples are required. Repeated calls add boxes to the same axis; outliers
# are optional and supplied separately.
import pykz

pykz.figure()
axis = pykz.ax(ylabel="Execution time (ms)")
pykz.boxplot(8, 10, 12, 15, 20, position=1, fill="cyan", ax=axis)
pykz.boxplot(
    5, 7, 9, 11, 14, position=2, outliers=[18, 21], fill="red", ax=axis
)
pykz.xticks([1, 2], ["Experiment A", "Experiment B"], ax=axis)
pykz.save("boxplot_comparison.tex", standalone=True)
pykz.io.export_pdf_from_file("boxplot_comparison.tex")

# %%
# For grouped comparisons, offset each method from the experiment's center
# and choose a width smaller than the spacing between methods. Keep colors
# consistent and label only the first box for each method to avoid duplicate
# legend entries. These are precomputed statistics, ordered from lower whisker
# through lower quartile, median, upper quartile, to upper whisker.
method_a = [(8, 10, 12, 15, 20), (11, 14, 17, 19, 24), (16, 20, 23, 27, 32)]
method_b = [(5, 7, 9, 11, 14), (8, 10, 12, 15, 19), (10, 13, 16, 20, 25)]

pykz.figure()
axis = pykz.ax(
    ylabel="Execution time (ms)", legend_pos="north west", width="12cm"
)
for center, (stats_a, stats_b) in enumerate(zip(method_a, method_b), start=1):
    pykz.boxplot(
        *stats_a, position=center - 0.18, width=0.28,
        fill="cyan", label="Method A" if center == 1 else None, ax=axis,
    )
    pykz.boxplot(
        *stats_b, position=center + 0.18, width=0.28,
        fill="red", label="Method B" if center == 1 else None, ax=axis,
    )
pykz.xticks([1, 2, 3], ["Experiment A", "Experiment B", "Experiment C"], ax=axis)
pykz.save("boxplot_grouped.tex", standalone=True)
pykz.io.export_pdf_from_file("boxplot_grouped.tex")

# %%
# Horizontal boxes use the same statistics. Positions now lie on the y axis,
# so label the groups with yticks instead of xticks.
pykz.figure()
axis = pykz.ax(xlabel="Execution time (ms)")
for position, stats in enumerate(method_a, start=1):
    pykz.boxplot(
        *stats, position=position, orientation="horizontal", fill="cyan", ax=axis
    )
pykz.yticks([1, 2, 3], ["Experiment A", "Experiment B", "Experiment C"], ax=axis)
pykz.save("boxplot_horizontal.tex", standalone=True)
pykz.io.export_pdf_from_file("boxplot_horizontal.tex")
