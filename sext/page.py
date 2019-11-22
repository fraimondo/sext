import numpy as np

from rpy2.robjects.packages import importr
from rpy2.robjects import numpy2ri


# import rpy2.robjects as ro


def pageTest(df, samples_col, measures, ascending=True):
    dt = importr('DescTools')
    values = df[measures].values
    if ascending is False:
        values = values[:, ::-1]
        # values = np.copy(values[:, ::-1])
    r_matrix = numpy2ri.numpy2ri(values)
    r_page = dt.PageTest(r_matrix)

    L = np.array(r_page.rx2('statistic'))[0]
    p = np.array(r_page.rx2('p.value'))[0]

    return L, p
