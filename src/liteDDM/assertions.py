from src.liteDDM.test_definitions import combined_distribution_test

'''
Assertions for liteDDM. These are the user-facing functions that 
raise errors when drift is detected.
'''

def assert_no_distribution_drift(df1, df2, alpha=0.05):
    import pandas as pd

    results, failures = combined_distribution_test(df1, df2, alpha)

    if failures:
        df_fail = pd.DataFrame(failures).sort_values("pvalue")

        raise AssertionError(
            f"Distribution drift detected (FDR α={alpha}):\n\n"
            f"{df_fail.to_string(index=False)}"
        )