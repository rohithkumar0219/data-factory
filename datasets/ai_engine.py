import numpy as np

def generate_ai_summary(df):
    summary = []
    summary.append(f"Dataset has {df.shape[0]} rows and {df.shape[1]} columns.")

    missing = df.isnull().sum()
    for col, count in missing.items():
        if count > 0:
            summary.append(f"{col}: {count} missing values")

    duplicates = df.duplicated().sum()
    if duplicates > 0:
        summary.append(f"{duplicates} duplicate rows found")

    numeric = df.select_dtypes(include=np.number)
    for col in numeric.columns:
        q1 = numeric[col].quantile(0.25)
        q3 = numeric[col].quantile(0.75)
        iqr = q3 - q1
        outliers = ((numeric[col] < q1 - 1.5 * iqr) |
                    (numeric[col] > q3 + 1.5 * iqr)).sum()
        if outliers > 0:
            summary.append(f"{outliers} potential outliers in column '{col}'")

    return "\n".join(summary)
