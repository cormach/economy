import re
import pandas as pd


def clean_date(bgs_index):
    if re.match(r"^\d{2}\s\w{3}\s+\d{4}$", bgs_index):
        return pd.to_datetime(bgs_index, format="%d %b %Y", errors="coerce")
    else:
        return pd.to_datetime(bgs_index)


def clean_percentage(x):
    if x.strip() in ["Variable", "Floating"]:
        return x
    try:
        x = float(x)
    except (ValueError, TypeError):
        units, fractions = x.split(" ")
        num, denom = map(float, fractions.split("/"))
        x = float(units) + num / denom
        print(x)
    return x
