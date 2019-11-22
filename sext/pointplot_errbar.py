import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def pointplot(x, y, hue, ax, data, order, markers='o', linestyles='-', error=None):
    all_lines = data[hue].unique()
    colors = sns.color_palette('husl', all_lines.shape[0])
    for i_line, line in enumerate(all_lines):
        this_data = data[data[hue] == line]
        x_ax = []
        y_ax = []
        y_err = []
        for i_x, x_label in enumerate(order):
            if np.sum(this_data[x] == x_label):
                y_ax.append(this_data[this_data[x] == x_label][y].values[0])
                if error is not None:
                    y_err.append(
                        this_data[this_data[x] == x_label][error].values[0])
                x_ax.append(i_x)

        ax.plot(x_ax, y_ax, color=colors[i_line], marker=markers,
                linestyle=linestyles, linewidth=0.5, markersize=3, label=line)
        if error is not None:
            ax.errorbar(x_ax, y_ax, yerr=y_err, ecolor=colors[i_line], capsize=3, capthick=1, fmt='none')

    ax.set_xticks(np.arange(len(order)))
    ax.set_xticklabels(order)
    ax.legend()
