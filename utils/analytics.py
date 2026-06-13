import pandas as pd


def top_product(df):
    if len(df) == 0:
        return "-"

    return df["Product"].mode()[0]


def top_reason(df):
    if len(df) == 0:
        return "-"

    return df["Reason"].mode()[0]


def top_city(df):
    if len(df) == 0:
        return "-"

    return df["City"].mode()[0]


def top_salesperson(df):
    if len(df) == 0:
        return "-"

    return df["Salesperson"].mode()[0]


def product_count(df):
    return df["Product"].value_counts()


def reason_count(df):
    return df["Reason"].value_counts()


def city_count(df):
    return df["City"].value_counts()


def salesperson_count(df):
    return df["Salesperson"].value_counts()