import pandas as pd

def normalize_column_names(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[^\w\s]", "", regex=True)
        .str.replace(r"\s+", "_", regex=True)
    )
    return df

def auto_clean(df):
    df = normalize_column_names(df)

    for col in df.columns:
        if "date" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce")
        elif "time" in col:
            df[col] = pd.to_datetime(df[col], format="%H:%M:%S.%f", errors="coerce").dt.time
        elif "postal" in col:
            df[col] = df[col].astype(str)
        elif set(df[col].dropna().unique()) <= {"Yes", "No"}:
            df[col] = df[col].map({"Yes": True, "No": False})
    return df
