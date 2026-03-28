import numpy as np
import pandas as pd


from scipy.stats import ks_2samp, chi2_contingency, anderson_ksamp

'''
Helper functions for distribution drift testing.
'''


def _test_column(x, y, col, use_anderson=True):
    '''
    Test if column `col` has distribution drift between x and y.
    - For categorical: chi2 test
    - For numeric: Anderson-Darling k-sample test (or KS as fallback)
    '''
    x = x.dropna()
    y = y.dropna()

    # Heuristic: categorical if dtype is object/category or few unique values
    is_categorical = (
        pd.api.types.is_object_dtype(x)
        or pd.api.types.is_categorical_dtype(x)
        or x.nunique() < 20
    )

    if is_categorical:
        # Align categories
        x_counts = x.value_counts()
        y_counts = y.value_counts()

        all_idx = x_counts.index.union(y_counts.index)

        x_counts = x_counts.reindex(all_idx, fill_value=0)
        y_counts = y_counts.reindex(all_idx, fill_value=0)

        table = np.vstack([x_counts.values, y_counts.values])

        _, pvalue, _, _ = chi2_contingency(table)

        return {
            "column": col,
            "test": "chi2",
            "pvalue": pvalue,
        }

    else:
        # Numeric
        if use_anderson:
            result = anderson_ksamp([x.values, y.values])
            pvalue = result.significance_level / 100.0  # convert %
            test_name = "anderson"
        else:
            _, pvalue = ks_2samp(x.values, y.values)
            test_name = "ks"

        return {
            "column": col,
            "test": test_name,
            "pvalue": pvalue,
        }
    

def benjamini_hochberg(pvalues, alpha=0.05):
    '''
    Apply Benjamini-Hochberg procedure for multiple testing correction.
    Returns boolean array of which hypotheses to reject.
    '''
    pvalues = np.array(pvalues)
    n = len(pvalues)

    # Sort p-values
    idx = np.argsort(pvalues)
    sorted_p = pvalues[idx]

    # Compute thresholds
    thresholds = alpha * (np.arange(1, n + 1) / n)

    # Find largest k where p_k <= threshold_k
    below = sorted_p <= thresholds
    if not np.any(below):
        return np.zeros(n, dtype=bool)

    k = np.max(np.where(below))
    cutoff = sorted_p[k]

    # Reject all p <= cutoff
    return pvalues <= cutoff