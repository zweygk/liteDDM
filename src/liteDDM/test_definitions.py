from src.liteDDM.helpers import benjamini_hochberg, _test_column
from hyppo.ksample import Energy
import numpy as np

'''
Test definitions for liteDDM. These are the core logic of the tests, 
without any assertions or error handling.
'''


def combined_distribution_test(df1, df2, alpha=0.05):
    '''
    Perform a combined distribution test between df1 and df2.
    - Multivariate test on all numeric columns (Energy test)
    - Univariate tests on each column (KS for numeric, chi2 for categorical)
    - Apply Benjamini-Hochberg correction for multiple testing
    Returns:
    - results: list of dicts with test results for each column and multivariate test
    - failures: list of dicts for tests that failed after FDR correction
    '''
    results = []

    # --- Multivariate test ---
    numerical_cols = df1.select_dtypes(include=[np.number]).columns
    if len(numerical_cols) > 1:  # Need at least 2 columns for multivariate
        stat, pvalue_mv = Energy().test(df1[numerical_cols].values, df2[numerical_cols].values)

        results.append({
            "column": "__multivariate__",
            "test": "energy",
            "pvalue": pvalue_mv,
        })

    # --- Column-wise tests ---
    for col in df1.columns:
        res = _test_column(df1[col], df2[col], col)
        results.append(res)

    # --- Apply FDR ---
    pvalues = [r["pvalue"] for r in results]
    reject_mask = benjamini_hochberg(pvalues, alpha)

    failures = [
        r for r, reject in zip(results, reject_mask) if reject
    ]

    return results, failures