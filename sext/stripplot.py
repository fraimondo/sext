import matplotlib.pyplot as plt
import seaborn as sns


def stripplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None,
              jitter=False, split=False, orient=None, color=None, palette=None,
              size=5, edgecolor='gray', linewidth=0, ax=None, annotate=None,
              kwargs={}):
    ax = sns.stripplot(
        x=x, y=y, hue=hue, data=data, order=order, hue_order=hue_order,
        jitter=jitter, split=split, orient=orient, color=color, palette=palette,
        size=size, edgecolor=edgecolor, linewidth=linewidth, ax=ax, **kwargs)

    if annotate is not None:
        x_group_labels = sns.utils.categorical_order(data.get(x, x))
        y_group_labels = sns.utils.categorical_order(data.get(y, y))
        t_orient = 'h' if str(orient).startswith('h') else 'v'
        if t_orient == 'h':
            group_labels = y_group_labels
            group = y
        else:
            group_labels = x_group_labels
            group = x

        for i_group, group_label in enumerate(group_labels):
            t_labels = data[data[group] == group_label][annotate]
            for label, (x, y) in zip(t_labels,
                                     ax.collections[i_group].get_offsets()):
                plt.annotate(label, xy=(x + 0.01, y + 0.01), alpha=0.7)
