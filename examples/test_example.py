from src.liteDDM.assertions import assert_no_distribution_drift
import pandas as pd
import numpy as np

'''
Example test using the liteDDM framework. 
'''

def test_mixed_dataframe():
    '''Test a mixed dataframe with both numeric and categorical columns.'''
    df1 = pd.DataFrame({
        "num1": np.random.normal(0, 1, 500),
        "num2": np.random.normal(0, 1, 500),
        "cat": np.random.choice(["A", "B"], 500),
    })

    df2 = pd.DataFrame({
        "num1": np.random.normal(0.5, 1, 500),  # shifted
        "num2": np.random.normal(0, 1, 500),
        "cat": np.random.choice(["A", "B"], 500),
    })

    assert_no_distribution_drift(df1, df2, alpha=0.05)