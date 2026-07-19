import pandas as pd

def load_data(path):
    return pd.read_csv(path)

def clean_throw_names(df):
    df["winner_throw"] = (
        df["winner_throw"]
        .str.strip()
        .str.title()
    )
    return df