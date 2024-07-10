import cython
import numpy as np
from statsmodels.tsa.stattools import adfuller

cpdef tuple cointegration_check(series01, series02):
    series01 = np.array(series01)
    series02 = np.array(series02)
    urt_1 = adfuller(series01, 1)[1]
    urt_2 = adfuller(series02, 1)[1]

    # 同时平稳或不平稳则差分再次检验
    if (urt_1 > 0.1 and urt_2 > 0.1) or (urt_1 < 0.1 and urt_2 < 0.1):
        urt_diff_1 = adfuller(np.diff(series01), 1)[1]
        urt_diff_2 = adfuller(np.diff(series02), 1)[1]

        # 同时差分平稳进行OLS回归的残差平稳检验
        if urt_diff_1 < 0.1 and urt_diff_2 < 0.1:
            matrix = np.vstack([series02, np.ones(len(series02))]).T
            beta, c = np.linalg.lstsq(matrix, series01, rcond=None)[0]
            resid = series01 - beta * series02 - c
            resid_mean = np.mean(resid)
            resid_std = np.std(resid)
            resid = list(resid)
            if adfuller(resid, 1)[1] > 0.1:
                result = False
            else:
                result = True
            return beta, c, resid_mean, resid_std, result
        else:
            result = False
            return 0.0, 0.0, 0.0, 0.0, result

    else:
        result = False
        return 0.0, 0.0, 0.0, 0.0, result


