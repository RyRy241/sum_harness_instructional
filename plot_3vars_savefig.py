"""
 
E. Wes Bethel, Copyright (C) 2022
October 2022
 
Modified for CSC 746 HW1 -- sum study (direct / vector / indirect).
 
Description: loads a .csv file of results and creates a 3-variable plot,
             displays it, and saves it as a .png
 
Usage:   python plot_3vars_savefig.py            # builds all three charts
         python plot_3vars_savefig.py mflops     # builds just one
         (valid names: mflops, bandwidth, latency)
 
Inputs:  mflops.csv, bandwidth.csv, latency.csv
Outputs: mflops.png, bandwidth.png, latency.png  (300 dpi)
 
Dependencies: matplotlib, pandas
 
"""
 
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
 
PLATFORM = ("Perlmutter CPU node: AMD EPYC 7763 (Milan), 1 core, "
            "GCC 7.5.0, -O1 -march=native, median of 3 runs")
 
CHARTS = {
    "mflops": {
        "fname":      "mflops.csv",
        "plot_fname": "mflops.png",
        "title":      "Sum Rate vs. Problem Size\nDirect, Vector, and Indirect Sum",
        "ylabel":     "Rate (MFLOP/s, log scale)",
        "logy":       True,
        "yticks":     [150, 200, 300, 500, 1000, 2000, 3000, 4000],
    },
    "bandwidth": {
        "fname":      "bandwidth.csv",
        "plot_fname": "bandwidth.png",
        "title":      ("Memory Bandwidth Utilization vs. Problem Size\n"
                       "Percent of 204.8 GB/s peak (one EPYC 7763 socket)"),
        "ylabel":     "Memory Bandwidth Utilized (% of peak)",
        "logy":       False,
        "yticks":     None,
    },
    "latency": {
        "fname":      "latency.csv",
        "plot_fname": "latency.png",
        "title":      ("Average Memory Latency vs. Problem Size\n"
                       "Elapsed time divided by number of memory accesses"),
        "ylabel":     "Average Memory Latency (ns per access)",
        "logy":       False,
        "yticks":     None,
    },
}
 
 
def size_label(n):
    """Turn a problem size into 'N' over its array footprint, e.g. 2 GB."""
    nbytes = n * 8                  
    if nbytes >= 1024 ** 3:
        foot = "%g GB" % (nbytes / 1024 ** 3)
    else:
        foot = "%g MB" % (nbytes / 1024 ** 2)
    return "%d\n(%s)" % (n, foot)
 
 
def make_chart(key):
    cfg = CHARTS[key]
 
    df = pd.read_csv(cfg["fname"], comment="#")
    print("--- " + cfg["fname"])
    print(df)
 
    var_names = list(df.columns)
    print("var names =", var_names)

    # column order - 0->problem size, 1->direct, 2->vector, 3->indirect
    problem_sizes = df[var_names[0]].values.tolist()
    code1_time = df[var_names[1]].values.tolist()
    code2_time = df[var_names[2]].values.tolist()
    code3_time = df[var_names[3]].values.tolist()
 
    plt.figure(figsize=(11.5, 6.5))
 
    plt.title(cfg["title"], fontsize=13)
 
    xlocs = [i for i in range(len(problem_sizes))]
    plt.xticks(xlocs, [size_label(n) for n in problem_sizes], fontsize=9)
 
    plt.plot(code1_time, "r-o")
    plt.plot(code2_time, "b-x")
    plt.plot(code3_time, "g-^")
 
    if cfg["logy"]:
        plt.yscale("log")
        # a log axis labels only the decades by default (a lone "10^3"), which
        # makes values impossible to read off; label useful values as plain
        # numbers instead
        ax = plt.gca()
        ax.set_yticks(cfg["yticks"])
        ax.yaxis.set_major_formatter(ScalarFormatter())
        ax.minorticks_off()
 
    plt.xlabel("Problem Size (N, number of 64-bit integers; array footprint in parentheses)")
    plt.ylabel(cfg["ylabel"])
 
    varNames = [var_names[1], var_names[2], var_names[3]]
    plt.legend(varNames, loc="upper left", bbox_to_anchor=(1.02, 1.0),
               borderaxespad=0.0, fontsize=10, title="Implementation",
               title_fontsize=10)
 
    plt.grid(axis='both')
 
    # provenance caption: a benchmark chart without its hardware and compiler
    # settings is not reproducible
    plt.figtext(0.42, 0.045, PLATFORM, ha="center", fontsize=8, style="italic")
 
    # reserve the right-hand margin for the legend. tight_layout() is not used
    # here because it only measures artists inside the axes and would clip a
    # legend placed outside them; bbox_inches="tight" at save time grows the
    # canvas to fit whatever ends up outside.
    plt.subplots_adjust(left=0.08, right=0.76, top=0.87, bottom=0.17)
 
    # save the figure before trying to show the plot
    plt.savefig(cfg["plot_fname"], dpi=300, bbox_inches="tight")
    print("wrote " + cfg["plot_fname"])
 
 
if len(sys.argv) > 1:
    requested = sys.argv[1:]
else:
    requested = list(CHARTS.keys())
 
for key in requested:
    if key not in CHARTS:
        print("unknown chart '%s'; valid names: %s" % (key, ", ".join(CHARTS)))
        sys.exit(1)
    make_chart(key)
 
plt.show()
 
# EOF