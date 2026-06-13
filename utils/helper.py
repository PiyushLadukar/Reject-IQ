from .data_manager import load_data, save_data


def total_records(df):
    return len(df)


def latest_records(df, n=5):
    if len(df) == 0:
        return df

    return df.tail(n).iloc[::-1]